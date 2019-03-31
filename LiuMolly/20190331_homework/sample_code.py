#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: sample_code
# @Date: 2019-03-31
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os
import sys
import warnings

import numpy as np
import pandas as pd
import xgboost as xgb
from statistics import mean
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


###############################################################################
# The function below construct the y and x variables for a given time period t##
###############################################################################
def yxdata(t, validdate, df, ranky, rankx):
    selected_date = validdate.iloc[t]
    lag_date = validdate.iloc[t - 1]
    cs = df.loc[(df['Date2'] == selected_date)]  # cross-sectional data for period t
    lag_cs = df.loc[(df['Date2'] == lag_date)]  # cross-sectional data for period t-1

    y_data = pd.DataFrame(data=cs[['returns', 'Stock', 'Date2']])
    y_data.rename(columns={'returns': 'yreturns'}, inplace=True)
    y_data.rename(columns={'Date2': 'yDate2'}, inplace=True)
    y_data = pd.merge(y_data, Stock300, on=['Stock'], how="outer")

    x_data1 = lag_cs
    x_data = pd.merge(x_data1, Stock300, on=['Stock'], how="outer")
    x_data.rename(columns={'returns': 'lag_ret'}, inplace=True)

    yx_data = pd.merge(y_data, x_data, on=['Stock'], how="outer")
    yx_data = yx_data.dropna(subset=['yreturns'])
    yx_data = yx_data.fillna(yx_data.mean())

    if ranky == 1:
        yx_data['yreturns'] = yx_data['yreturns'].rank(ascending=0)

    if rankx == 1:
        x_variable_names1 = x_variable_names[0:-2]
        yx_data[x_variable_names1] = yx_data[x_variable_names1].rank(ascending=0)

    return yx_data


def show_corrs(pred_y, test_y):
    comdf = pd.DataFrame({'pred_y': pred_y[:, 0], 'test_y': test_y[:, 0]})
    comdf['pred_y_rank'] = comdf['pred_y'].rank(ascending=0)
    comdf['test_y_rank'] = comdf['test_y'].rank(ascending=0)
    rank_corr = comdf['pred_y_rank'].corr(comdf['test_y_rank'])
    return_corr = comdf['pred_y'].corr(comdf['test_y'])
    return rank_corr, return_corr


if __name__ == '__main__':
    plt.style.use('seaborn-white')

    filename = os.path.join('/Users/warn/Google Drive/LiuMolly/20190331_homework',
                            '20190313 82 variables 300 stocks.csv')
    df = pd.read_csv(filename)

    df = df.dropna(subset=['SYMBOL', 'PCT_RET', 'VOLUME'])

    df['returns'] = df['PCT_RET']
    df['Date2'] = pd.to_datetime(df.DATE)
    df['Stock'] = df['SYMBOL']

    period = pd.unique(df.Date2)  # this is all the tiem periods in the dataset
    period = np.sort(period)
    stocks = pd.unique(df.SYMBOL)  # this is all the stock in the dataset
    # stocks=np.delete(stocks,4,axis=0)

    gen_industry_dummy = 1  # generate industry dummies
    if gen_industry_dummy == 1:
        df = pd.get_dummies(df, columns=['SIC2'])
        all_variables = list(df)
        industry_variables = all_variables[-17:]
    else:
        industry_variables = []

    #######################################################################
    # Check missing data (some periods may have few stocks (less than 100))#
    #######################################################################

    T0 = period.size
    stock_number_each_period = []
    for i in range(T0):
        data2 = df.loc[(df['Date2'] == period[i]), ['returns']]
        stock_number_each_period.append(len(data2) - data2.returns.isna().sum())

    stock_number_each_period2 = pd.DataFrame(data=stock_number_each_period)
    stock_number_each_period2['period'] = period
    stock_number_each_period2.columns = ['number of stocks', 'period']
    validdate = stock_number_each_period2.loc[(stock_number_each_period2['number of stocks'] > 100), 'period']
    validdate_value = validdate.values

    T = validdate_value.size
    Stock300 = pd.DataFrame(data=stocks)
    Stock300.columns = ['Stock']

    ###############################################################################
    ##########################Foecasting ##########################################
    ###############################################################################

    x_variable_selection = ['MOM12M', 'CHMOM', 'MAXRET', 'RETVOL', 'DOLVOL', 'SP', 'STD_TURN', 'MOM6M', 'MKT_CAP',
                            'MOM1M',
                            'MOM36M', 'DY']

    x_variable_names = x_variable_selection[:]
    if gen_industry_dummy == 1:
        x_variable_names.extend(industry_variables)

    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    ranky = 0  # whether you want to transform y variable to ranks
    rankx = 0  # whether you want to transform x variables to ranks
    standardized = 1  # whether you want to standardize data

    test_period = 24  # the number of peridos for testing
    lag_period = 3  # the number of periods used in the training

    saved_corr = []

    for t in range(T - test_period, T):
        train_data = yxdata(t - 1, validdate, df, ranky, rankx)
        for lagt in range(2, lag_period):
            temp_train_data = yxdata(t - lagt, validdate, df, ranky, rankx)
            train_data = pd.concat([train_data, temp_train_data])

        test_data = yxdata(t, validdate, df, ranky, rankx)

        train_y = train_data['yreturns'].values.reshape(-1, 1)
        test_y = test_data['yreturns'].values.reshape(-1, 1)

        train_x = train_data[x_variable_names].values
        test_x = test_data[x_variable_names].values

        if standardized == 1:
            scalar = StandardScaler().fit(train_x)
            train_x = scalar.transform(train_x)
            test_x = scalar.transform(test_x)

        method = xgb.XGBRegressor(objective='reg:linear', colsample_bytree=0.25, learning_rate=0.002, max_depth=5,
                                  alpha=50, n_estimators=5000, random_state=0)
        method.fit(train_x, train_y)
        pred_y = method.predict(test_x)
        pred_y = pred_y.reshape(-1, 1)

        rank_corr, return_corr = show_corrs(pred_y, test_y)
        saved_corr.append(rank_corr)

    print('mean_corr=', mean(saved_corr))

    plt.plot(validdate[T - test_period - 1:T - 1], saved_corr, 'b-.+')
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.show()
