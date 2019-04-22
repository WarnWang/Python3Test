#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: sample_code
# @Date: 2019-04-21
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os
import sys
import warnings

import pandas as pd
import numpy as np
from tqdm import trange
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from matplotlib.legend_handler import HandlerLine2D

if not sys.warnoptions:
    warnings.simplefilter("ignore")


def yxdata(t, validdate, df, ranky, rankx):
    selected_date = validdate.iloc[t]

    cs = df.loc[(df['Date2'] == selected_date)]  # cross-sectional data for period t

    y_data = pd.DataFrame(data=cs[['returns', 'Stock', 'Date2', 'industry', 'CSI_PCT_RET']])
    y_data.rename(columns={'returns': 'yreturns'}, inplace=True)
    y_data.rename(columns={'Date2': 'yDate2'}, inplace=True)
    y_data.rename(columns={'industry': 'yindustry'}, inplace=True)
    y_data.rename(columns={'CSI_PCT_RET': 'yCSI_PCT_RET'}, inplace=True)
    y_data = pd.merge(y_data, Stock300, on=['Stock'], how="outer")

    lag_date = validdate.iloc[t - 1]
    lag_cs = df.loc[(df['Date2'] == lag_date)]  # cross-sectional data for period t-1
    x_data1 = lag_cs
    x_data1 = pd.merge(x_data1, Stock300, on=['Stock'], how="outer")
    x_data1.rename(columns={'returns': 'lag1_returns'}, inplace=True)
    x_data1.rename(columns={'CSI_PCT_RET': 'lag1_CSI_PCT_RET'}, inplace=True)

    lag2_date = validdate.iloc[t - 2]
    lag_cs2 = df.loc[(df['Date2'] == lag2_date)]  # cross-sectional data for period t-2
    x_data2 = lag_cs2[['Stock', 'returns', 'CSI_PCT_RET']]
    x_data2.rename(columns={'returns': 'lag2_returns'}, inplace=True)
    x_data2.rename(columns={'CSI_PCT_RET': 'lag2_CSI_PCT_RET'}, inplace=True)
    x_data2 = pd.merge(x_data2, Stock300, on=['Stock'], how="outer")

    lag3_date = validdate.iloc[t - 3]
    lag_cs3 = df.loc[(df['Date2'] == lag3_date)]  # cross-sectional data for period t-3
    x_data3 = lag_cs3[['Stock', 'returns', 'CSI_PCT_RET']]
    x_data3.rename(columns={'returns': 'lag3_returns'}, inplace=True)
    x_data3.rename(columns={'CSI_PCT_RET': 'lag3_CSI_PCT_RET'}, inplace=True)
    x_data3 = pd.merge(x_data3, Stock300, on=['Stock'], how="outer")

    x_data12 = pd.merge(x_data1, x_data2, on=['Stock'], how="outer")
    x_data = pd.merge(x_data12, x_data3, on=['Stock'], how="outer")

    yx_data = pd.merge(y_data, x_data, on=['Stock'], how="outer")
    yx_data = yx_data.dropna(subset=['yreturns'])
    yx_data = yx_data.dropna(subset=['lag1_returns'])
    yx_data = yx_data.dropna(subset=['lag2_returns'])
    yx_data = yx_data.dropna(subset=['lag3_returns'])

    yx_data = yx_data.fillna(yx_data.mean())

    if ranky == 1:
        yx_data['yreturns'] = yx_data['yreturns'].rank(ascending=0)

    if rankx == 1:
        x_variable_names1 = x_variable_names[0:-2]
        yx_data[x_variable_names1] = yx_data[x_variable_names1].rank(ascending=0)

    return yx_data


def long_short(pred_y, testdata, K):
    N = pred_y.shape[0]
    testdata['pred_y'] = pred_y
    testdata['test_y'] = testdata['yreturns']
    testdata['pred_y_rank'] = testdata['pred_y'].rank(ascending=0)
    testdata['test_y_rank'] = testdata['test_y'].rank(ascending=0)
    topK_stock = testdata.loc[testdata['pred_y_rank'] < (K + 1)]
    bottomK_stock = testdata.loc[testdata['pred_y_rank'] > (N - K)]

    if len(topK_stock.axes[0]) == 0:
        topK_stock = testdata.loc[testdata['pred_y_rank'] == testdata['pred_y_rank'].min()]

    if len(bottomK_stock.axes[0]) == 0:
        bottomK_stock = testdata.loc[testdata['pred_y_rank'] == testdata['pred_y_rank'].max()]

    topKreturn = topK_stock.test_y.mean()
    bottomKreturn = bottomK_stock.test_y.mean()
    marketreturn = testdata.yCSI_PCT_RET.mean()
    rank_corr = testdata['pred_y_rank'].corr(testdata['test_y_rank'])
    return_corr = testdata['pred_y'].corr(testdata['test_y'])

    LS_Kreturn = topKreturn - bottomKreturn

    return topKreturn, LS_Kreturn, marketreturn, rank_corr, return_corr, topK_stock, bottomK_stock


if __name__ == '__main__':
    plt.style.use('seaborn-white')

    filename = os.path.join('/Users/warn/Google Drive/LiuMolly/20190420_homework',
                            '20190328 102 variables 300 stocks.csv')
    df = pd.read_csv(filename)

    df = df.dropna(subset=['SYMBOL', 'PCT_RET', 'VOLUME'])
    df['industry'] = df['SIC2']
    df['returns'] = df['PCT_RET']
    df['Date2'] = pd.to_datetime(df.DATE)
    df['Stock'] = df['SYMBOL']

    period = pd.unique(df.Date2)  # this is all the time periods in the dataset
    period = np.sort(period)
    stocks = pd.unique(df.SYMBOL)  # this is all the stock in the dataset
    # stocks=np.delete(stocks,4,axis=0)

    genindustrydummy = 1
    if genindustrydummy == 1:
        df = pd.get_dummies(df, columns=['SIC2'])
        allvariables = list(df)
        industryvariable = allvariables[-17:]

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

    x_variable_selection = ['MKT_CAP', 'RETVOL', 'CHMOM', 'MAXRET', 'DOLVOL', 'MOM6M', 'ILL']

    ranky = 0
    rankx = 0
    standardized = 1
    test_period = 60
    lag_period = 2

    top10returns = np.zeros(test_period)
    LS10returns = np.zeros(test_period)
    rankcorr = np.zeros(test_period)
    returncorr = np.zeros(test_period)
    market_returns = np.zeros(test_period)

    x_variable_names = x_variable_selection

    if genindustrydummy == 1:
        x_variable_names = list(set(x_variable_names + industryvariable))

    tt = -1

    for t in trange(T - test_period, T):
        tt = tt + 1
        traindata = yxdata(t - 1, validdate, df, ranky, rankx)
        for lagt in range(2, lag_period + 1):
            temptraindata = yxdata(t - lagt, validdate, df, ranky, rankx)
            traindata = pd.concat([traindata, temptraindata])

        testdata = yxdata(t, validdate, df, ranky, rankx)

        train_y = traindata['yreturns'].values.reshape(-1, 1)
        train_x = traindata[x_variable_names].values
        test_x = testdata[x_variable_names].values

        na1 = np.where(np.isnan(np.sum(train_x, axis=0)) == True)
        na2 = np.where(np.isnan(np.sum(test_x, axis=0)) == True)
        na12 = np.union1d(np.array(na1), np.array(na2))
        train_x = np.delete(train_x, na12, 1)
        test_x = np.delete(test_x, na12, 1)

        if standardized == 1:
            scaler = StandardScaler().fit(train_x)
            train_x = scaler.transform(train_x)
            test_x = scaler.transform(test_x)

        mean = np.mean(train_y, axis=0)
        sd = np.std(train_y, axis=0)
        train_y = np.array(train_y)
        cconst = 2
        train_y[train_y > (mean + cconst * sd)] = mean + cconst * sd
        train_y[train_y < (mean - cconst * sd)] = mean - cconst * sd

        method = MLPRegressor(hidden_layer_sizes=(250), random_state=0)
        method.fit(train_x, train_y)
        pred_y = method.predict(test_x)
        pred_y = pred_y.reshape(-1, 1)

        t_top10return, t_LS_10return, t_marketreturn, t_rankcorr, t_return_corr, t_top10_stock, t_bottom10_stock = long_short(
            pred_y, testdata, 10)

        top10returns[tt] = t_top10return
        LS10returns[tt] = t_LS_10return
        rankcorr[tt] = t_rankcorr
        returncorr[tt] = t_return_corr
        market_returns[tt] = t_marketreturn

    result_df: pd.DataFrame = pd.DataFrame({'top10': top10returns, 'long-short': LS10returns, 'rank_corr': rankcorr,
                                            'return_corr': returncorr, 'mkt_returns': market_returns},
                                           columns=['top10', 'long-short', 'rank_corr', 'return_corr', 'mkt_returns'],
                                           index=validdate[T - test_period:])
    result_df.to_excel(os.path.join('/Users/warn/Google Drive/LiuMolly/20190420_homework',
                                    'result.xlsx'))

    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    print('top 10 returns:', np.mean(top10returns))
    print('long short 10 returns:', np.mean(LS10returns))
    print('market:', np.mean(market_returns))
    print('rank correlation:', np.mean(rankcorr))
    print('return correlation:', np.mean(returncorr))

    # draw figure 1
    line1, = plt.plot(validdate[T - test_period - 1:T - 1], market_returns, 'r-+', label='CSI 300 index')
    line2, = plt.plot(validdate[T - test_period - 1:T - 1], LS10returns, 'b*', label='Long-short top 10')

    plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.show()

    # draw figure 2
    plt.figure()
    line1, = plt.plot(validdate[T - test_period - 1:T - 1], market_returns, 'r-+', label='CSI 300 index')
    line2, = plt.plot(validdate[T - test_period - 1:T - 1], top10returns, 'b*', label='Long top 10')

    plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.show()

    # draw figure 3
    plt.figure()
    line1, = plt.plot(validdate[T - test_period - 1:T - 1], rankcorr, 'b*', label='Rank correlation')

    plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.show()
