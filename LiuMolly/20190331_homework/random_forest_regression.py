#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: random_forest_regression
# @Date: 2019-03-31
# @Author: Molly Liu
# @Email: wangyouan@gamil.com


import os
from datetime import datetime

import pandas as pd
from pandas import DataFrame
from tqdm import tqdm
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

# Random forest regression
from sklearn.ensemble import RandomForestRegressor

# Define variables
STOCK_SYMBOL = 'SYMBOL'
DATE = 'DATE'
RETURN = 'PRICE_CHG'
RETURN_1 = 'returns_1'
PREDICT_RETURN_1 = 'predict_return_1'
PREDICT_RANK = 'predict_rank'
REAL_RANK = 'real_rank'

# some parameters hear
window_size = 4

# variable name that will be used in regression you can choose which variables used for x
x_vars = ['VOLUME', 'AMT', 'PRICE_CHG', 'PCT_RET', 'AVG_PRICE', 'TURNOVER', 'MKT_CAP', 'ISSUED_SHARE', 'PB(HPS)',
          'PCF', 'PB', 'PE_T12MOB', 'PSALES', 'EPSY_FY0', 'TRL_YLD', 'RTN12_1M', 'RTN252D',
          'MA_CO_15_36W', 'REAL_VOL_1YD', 'SKEW_1YD', 'CFY_IS', 'CFROC_CF', 'SHORT_COV',
          'MOM1M', 'MOM12M', 'INDMOM', 'MAXRET', 'CHMOM', 'RETVOL', 'DOLVOL', 'MOM6M', 'SP', 'TURN', 'STD_TURN',
          'ILL', 'EP', 'MOM36M', 'ZEROTRADE', 'BM', 'BM_IA']
y_var = RETURN_1

tqdm.pandas()
register_matplotlib_converters()


# generate a shift to return, used for train and prediction
def get_next_return(df):
    df[RETURN_1] = df[RETURN].shift(-1)
    return df


if __name__ == '__main__':
    plt.style.use('seaborn-white')

    filename = os.path.join('/Users/warn/Google Drive/LiuMolly/20190331_homework',
                            '20190313 82 variables 300 stocks.csv')
    data_df: DataFrame = pd.read_csv(filename)

    data_df_add_next_return = data_df.groupby(STOCK_SYMBOL).progress_apply(get_next_return).reset_index(drop=True)

    # this are useful numeric variables
    numeric_vars = x_vars[:]
    numeric_vars.append(y_var)

    useful_vars = numeric_vars[:]
    useful_vars.extend([STOCK_SYMBOL, DATE])

    # only keep useful data
    data_df_useful = data_df_add_next_return[useful_vars].copy()

    # change data type
    data_df_useful.loc[:, DATE] = pd.to_datetime(data_df_useful[DATE])
    for key in numeric_vars:
        data_df_useful.loc[:, key] = pd.to_numeric(data_df_useful[key], errors='coerce')

    # split data to prepare for train and test
    data_df_useful = data_df_useful.dropna(how='any')
    date_list = data_df_useful[DATE].drop_duplicates().sort_values().to_list()
    test_date_list = date_list[-25:]

    predict_result = pd.DataFrame(columns=[STOCK_SYMBOL])
    real_result = pd.DataFrame(columns=[STOCK_SYMBOL])

    for date_index in tqdm(range(25, 1, -1)):
        train_date_list = date_list[-(date_index + window_size):-date_index]
        test_date: datetime = date_list[-date_index]
        target_date: datetime = date_list[-(date_index - 1)]

        train_data_df: DataFrame = data_df_useful.loc[data_df_useful[DATE].isin(set(train_date_list))].copy()
        test_data_df: DataFrame = data_df_useful.loc[data_df_useful[DATE] == test_date].copy()

        # training model and use the model to predict return
        rf = RandomForestRegressor(max_depth=4, random_state=0, n_estimators=100)
        reg = rf.fit(train_data_df[x_vars], train_data_df[y_var])
        test_data_df.loc[:, PREDICT_RETURN_1] = reg.predict(test_data_df[x_vars])
        test_data_df.loc[:, PREDICT_RANK] = test_data_df[PREDICT_RETURN_1].rank(ascending=False)
        test_data_df.loc[:, REAL_RANK] = test_data_df[RETURN_1].rank(ascending=False)
        predict_result: pd.DataFrame = predict_result.merge(
            test_data_df[[STOCK_SYMBOL, PREDICT_RANK]].rename(columns={PREDICT_RANK: target_date.strftime('%Y%m%d')}),
            on=[STOCK_SYMBOL], how='outer')
        real_result: pd.DataFrame = real_result.merge(
            test_data_df[[STOCK_SYMBOL, REAL_RANK]].rename(columns={REAL_RANK: target_date.strftime('%Y%m%d')}),
            on=[STOCK_SYMBOL], how='outer')

    corr = real_result.corrwith(predict_result)
    print('mean correlation =', corr.mean())
    plt.plot(test_date_list[1:], corr, 'b-.')

    plt.xticks(rotation=90)
    plt.show()
