#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: stop_rule_code
# @DATE: 2019-05-04
# @Author: Mark Wang
# @Email: wangyouan@gamil.com


import numpy as np
import pandas as pd
from tqdm import tqdm
from pandas import DataFrame
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import AdaBoostRegressor
from sklearn.linear_model import LassoCV

# unit is month
test_period = 120

# unit is day. e.g. N means use las N day data to train.
training_period = 30

# variable used for training
x_variable_selection = ['MKT_CAP', 'RETVOL', 'CHMOM', 'MAXRET', 'DOLVOL', 'MOM6M', 'ILL', 'MOM12M', 'MOM1M', 'MOM36M']

# clear all position when the portfolio return is lower than this value
stop_cum_return = -2
stop_daily_return = -4

standardized = 1

portfolio_size = 5


def separate_each_month_into_4_parts(sub_date_list: pd.Series):
    if sub_date_list.shape[0] < 20:
        sep_dfs = np.array_split(sub_date_list, 3)
    else:
        sep_dfs = np.array_split(sub_date_list, 4)

    for i, sub_series in enumerate(sep_dfs):
        sub_df = sub_series.to_frame(name='DATE')
        sub_df.loc[:, 'sep_num'] = i + 1
        sep_dfs[i] = sub_df

    return pd.concat(sep_dfs)


if __name__ == '__main__':
    tqdm.pandas()
    filename = '20190403 53 variables 300 stocks Daily.csv'
    df = pd.read_csv(filename)
    df_valid = df.dropna(subset=['SYMBOL', 'PCT_RET', 'VOLUME'])
    df_valid.loc[:, 'DATE'] = pd.to_datetime(df.DATE)
    df_valid.loc[:, 'year'] = df_valid['DATE'].dt.year
    df_valid.loc[:, 'month'] = df_valid['DATE'].dt.month

    month_list = df_valid.loc[:, ['year', 'month']].drop_duplicates().sort_values(by=['year', 'month'], ascending=True)
    valid_date_list = df_valid['DATE'].sort_values(ascending=True).drop_duplicates()
    valid_date_df: DataFrame = valid_date_list.to_frame()
    valid_date_df.loc[:, 'month'] = valid_date_df['DATE'].dt.month
    valid_date_df.loc[:, 'year'] = valid_date_df['DATE'].dt.year
    valid_date_with_sep_num: DataFrame = valid_date_df.groupby(['year', 'month'])['DATE'].progress_apply(
        separate_each_month_into_4_parts)

    df_valid_sep_temp: DataFrame = df_valid.merge(valid_date_with_sep_num, on=['DATE']).sort_values(by=['DATE'],
                                                                                                    ascending=True)

    # the following code is used to get stocks tomorrow return
    df_valid_sep_temp.loc[:, 'PCT_RET_1'] = df_valid_sep_temp.groupby(['SYMBOL'])['PCT_RET'].shift(-1)

    # only keep useful variables
    useful_variables = x_variable_selection[:]
    useful_variables.extend(['PCT_RET_1', 'PCT_RET', 'SYMBOL', 'year', 'month', 'DATE', 'sep_num'])
    df_valid_sep: DataFrame = df_valid_sep_temp.loc[:, useful_variables]

    return_df = DataFrame(columns=['year', 'month', 'month_return_ls', 'month_return_l'])

    for i in tqdm(month_list.index[-test_period:]):
        year = month_list.loc[i, 'year']
        month = month_list.loc[i, 'month']

        test_data = df_valid_sep.loc[(df_valid_sep['year'] == year) & (df_valid_sep['month'] == month)].copy()

        month_return = 0
        month_return_l = 0

        for period_index in test_data['sep_num'].drop_duplicates():
            period_data_df = test_data.loc[test_data['sep_num'] == period_index].dropna(
                subset=x_variable_selection, how='any')
            period_start_date, period_end_date = period_data_df['DATE'].min(), period_data_df['DATE'].max()
            period_stock_set = set(period_data_df['SYMBOL'])

            stock_select_df: DataFrame = df_valid_sep.loc[
                df_valid_sep['DATE'] == valid_date_list[valid_date_list < period_start_date].max()]
            stock_select_df: DataFrame = stock_select_df.loc[stock_select_df['SYMBOL'].isin(period_stock_set)]

            train_date_set = set(valid_date_list[valid_date_list < period_start_date][-test_period - 1: -1])
            training_data_df = df_valid_sep.loc[df_valid_sep['DATE'].isin(train_date_set)]

            # only keep those stocks has current date
            valid_training_df = training_data_df.loc[training_data_df['SYMBOL'].isin(set(period_stock_set))].dropna(
                subset=x_variable_selection, how='any')

            train_y = valid_training_df['PCT_RET_1'].values.reshape(-1, 1)
            train_x = valid_training_df[x_variable_selection].values
            test_x = stock_select_df.loc[:, x_variable_selection].values
            na1 = np.where(np.isnan(np.sum(train_x, axis=0)))
            na2 = np.where(np.isnan(np.sum(test_x, axis=0)))
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

            # method = AdaBoostRegressor(n_estimators=500, learning_rate=0.01, random_state=1)
            method = LassoCV(cv=5, random_state=0)
            method.fit(train_x, train_y)
            pred_y = method.predict(test_x).reshape(-1, 1)

            stock_select_df.loc[:, 'PRED_RET'] = pred_y

            sorted_stock_values = stock_select_df.sort_values(by=['PRED_RET'])
            positive_return_stocks = sorted_stock_values.loc[sorted_stock_values['PRED_RET'] > 0]
            negative_return_stocks = sorted_stock_values.loc[sorted_stock_values['PRED_RET'] < 0]

            top_k_stocks = set(positive_return_stocks.iloc[:portfolio_size]['SYMBOL'])
            bottom_k_stocks = set(negative_return_stocks.iloc[-portfolio_size:]['SYMBOL'])

            long_short_period = period_data_df['DATE'].drop_duplicates().sort_values(ascending=True)

            cum_ret = 0
            cum_ret_l = 0
            no_ls_flag = False
            no_l_flag = False

            for date_i in long_short_period:
                if cum_ret < stop_cum_return:
                    no_ls_flag = True

                if cum_ret_l < stop_cum_return:
                    no_l_flag = True

                if no_l_flag and no_ls_flag:
                    break

                long_stock_data = period_data_df.loc[
                    (period_data_df['DATE'] == date_i) & period_data_df['SYMBOL'].isin(top_k_stocks)]
                long_return = long_stock_data['PCT_RET'].mean()

                short_stock_data = period_data_df.loc[
                    (period_data_df['DATE'] == date_i) & period_data_df['SYMBOL'].isin(bottom_k_stocks)]
                short_return = short_stock_data['PCT_RET'].mean()

                if np.isnan(long_return):
                    long_return = 0

                if np.isnan(short_return):
                    short_return = 0

                long_short_ret = long_return - short_return
                if not no_ls_flag:
                    cum_ret = ((1 + cum_ret / 100) * (1 + long_short_ret / 100) - 1) * 100

                if not no_l_flag:
                    cum_ret_l = ((1 + cum_ret / 100) * (1 + long_return / 100) - 1) * 100

                if long_short_ret < stop_daily_return:
                    no_ls_flag = True

                if long_return < stop_daily_return:
                    no_l_flag = True

            month_return = ((1 + month_return / 100) * (1 + cum_ret / 100) - 1) * 100
            month_return_l = ((1 + month_return_l / 100) * (1 + cum_ret_l / 100) - 1) * 100

        return_df: DataFrame = return_df.append({'month': month, 'year': year, 'month_return_ls': month_return,
                                                 'month_return_l': month_return_l},
                                                ignore_index=True)
    return_df.to_csv('monthly_return.csv', index=False)
