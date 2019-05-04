#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: sample_code
# @Date: 2019-05-04
# @Author: Mark Wang
# @Email: wangyouan@gamil.com


import sys
import warnings

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import AdaBoostRegressor
from matplotlib.legend_handler import HandlerLine2D

if not sys.warnoptions:
    warnings.simplefilter("ignore")

# get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use('seaborn-white')

filename = 'D:/wind/data.csv'
df = pd.read_csv(filename)
df = df.dropna(subset=['SYMBOL', 'PCT_RET', 'VOLUME'])
df['returns'] = df['PCT_RET']
df['Date2'] = pd.to_datetime(df.DATE)
df['Stock'] = df['SYMBOL']

df['week'] = df['Date2'].dt.week
df['year'] = df['Date2'].dt.year

df_week_rtn = df.groupby(['year', 'week', 'SYMBOL']).sum()['PCT_RET'].reset_index()

df_week_date = df.drop_duplicates(subset=['year', 'week', 'SYMBOL'])

del df_week_date['PCT_RET']
df_week = df_week_rtn.merge(df_week_date, on=['year', 'week', 'SYMBOL'])

df = df_week
df['month'] = df['Date2'].dt.month

df['returns'] = df['PCT_RET']

period = pd.unique(df.Date2)  # this is all the time periods in the dataset
period = np.sort(period)
stocks = pd.unique(df.SYMBOL)  # this is all the stock in the dataset
stocks = np.delete(stocks, 4, axis=0)

T0 = period.size
stock_number_each_period = []

for i in range(T0):
    data2 = df.loc[(df['Date2'] == period[i]), ['returns']]
    stock_number_each_period.append(len(data2) - data2.returns.isna().sum())

i = T0

stock_number_each_period2 = pd.DataFrame(data=stock_number_each_period)
stock_number_each_period2['period'] = period
stock_number_each_period2.columns = ['number of stocks', 'period']
validdate = stock_number_each_period2.loc[(stock_number_each_period2['number of stocks'] > 100), 'period']
validdate_value = validdate.values

T = validdate_value.size
Stock300 = pd.DataFrame(data=stocks)
Stock300.columns = ['Stock']


def yxdata(t, validdate, df, ranky, rankx):
    selected_date = validdate.iloc[t]

    cs = df.loc[(df['Date2'] == selected_date)]  # cross-sectional data for period t

    y_data = pd.DataFrame(data=cs[['returns', 'Stock', 'Date2']])
    y_data.rename(columns={'returns': 'yreturns'}, inplace=True)
    y_data.rename(columns={'Date2': 'yDate2'}, inplace=True)
    y_data = pd.merge(y_data, Stock300, on=['Stock'], how="outer")

    lag_date = validdate.iloc[t - 1]
    lag_cs = df.loc[(df['Date2'] == lag_date)]  # cross-sectional data for period t-1
    x_data1 = lag_cs
    x_data1 = pd.merge(x_data1, Stock300, on=['Stock'], how="outer")
    x_data1.rename(columns={'returns': 'lag1_returns'}, inplace=True)

    lag2_date = validdate.iloc[t - 2]
    lag_cs2 = df.loc[(df['Date2'] == lag2_date)]  # cross-sectional data for period t-2
    x_data2 = lag_cs2[['Stock', 'returns']]
    x_data2.rename(columns={'returns': 'lag2_returns'}, inplace=True)
    x_data2 = pd.merge(x_data2, Stock300, on=['Stock'], how="outer")

    x_data = pd.merge(x_data1, x_data2, on=['Stock'], how="outer")

    yx_data = pd.merge(y_data, x_data, on=['Stock'], how="outer")
    yx_data = yx_data.dropna(subset=['yreturns'])
    yx_data = yx_data.dropna(subset=['lag1_returns'])
    yx_data = yx_data.dropna(subset=['lag2_returns'])

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
    rank_corr = testdata['pred_y_rank'].corr(testdata['test_y_rank'])
    return_corr = testdata['pred_y'].corr(testdata['test_y'])

    LS_Kreturn = topKreturn - bottomKreturn

    return topKreturn, LS_Kreturn, rank_corr, return_corr, topK_stock, bottomK_stock


x_variable_selection = ['MKT_CAP', 'RETVOL', 'CHMOM', 'MAXRET', 'DOLVOL', 'MOM6M', 'ILL', 'MOM12M', 'MOM1M', 'MOM36M']

ranky = 0
rankx = 0
standardized = 1
test_period = 30
lag_period = 1

top5returns = np.zeros((test_period, 1))
LS5returns = np.zeros((test_period, 1))
rankcorr = np.zeros((test_period, 1))
returncorr = np.zeros((test_period, 1))

x_variable_names = x_variable_selection

tt = -1

for t in range(T - test_period, T):
    traindata = yxdata(t - 1, validdate, df, ranky, rankx)
    for lagt in range(2, lag_period + 1):
        temptraindata = yxdata(t - lagt, validdate, df, ranky, rankx)
        traindata = pd.concat([traindata, temptraindata])

    testdata = yxdata(t, validdate, df, ranky, rankx)
    train_y = traindata['yreturns'].values.reshape(-1, 1)
    train_x = traindata[x_variable_names].values
    test_x = testdata[x_variable_names].values
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

    method = AdaBoostRegressor(n_estimators=500, learning_rate=0.01 * (i + 1), random_state=1)
    method.fit(train_x, train_y)
    pred_y = method.predict(test_x)
    pred_y = pred_y.reshape(-1, 1)

    t_top5return, t_LS_5return, t_rankcorr, t_return_corr, t_top5_stock, t_bottom5_stock = long_short(pred_y, testdata,
                                                                                                      5)

    top5returns[tt, 0] = t_top5return
    LS5returns[tt, 0] = t_LS_5return
    rankcorr[tt, 0] = t_rankcorr
    returncorr[tt, 0] = t_return_corr

print('top 5 returns:', np.mean(top5returns))
print('long short 5 returns:', np.mean(LS5returns))
print('rank correlation:', np.mean(rankcorr))
print('return correlation:', np.mean(returncorr))

line2, = plt.plot(validdate[T - test_period - 1:T - 1], LS5returns, 'b*', label='Long-short top 5')

plt.legend(handler_map={line2: HandlerLine2D(numpoints=4)})
plt.grid(True)
plt.xticks(rotation=90)
plt.show()
