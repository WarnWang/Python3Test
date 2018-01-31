#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: cumulative_abnormal_returns
# @Date: 31/1/2018
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os

import pandas as pd
import numpy as np
import statsmodels.api as sm


def car(stock_return_series, event_date, factor_number, period_start_days, period_end_days, ff_factor_path):
    """
    To calculate the cumulative abnormal return.
    Input stock ticker, event date, factor number, and test interval.
    Factor number must be 1, 3 or 4. The default value of test interval is set to 5.
    @:param stock_symbol could be cusip or stock ticker

    if calculate CAR, period_start_days should be -2 and period_end_days should be 2
    if calculate RUN up, period_start_days should be -210 and period_end_days should be -11
    """
    if factor_number not in {1, 3, 4}:
        # print('Factor number must be 1, 3, 4')
        return np.nan, 'Invalid factor number'

    if period_start_days > period_end_days:
        return np.nan, 'Invalid period days'

    ff_4_factor_df = pd.read_pickle(ff_factor_path)

    useful_col = ['Mkt-RF', 'SMB', 'HML', 'Mom'][:factor_number]
    ff_factor_df = ff_4_factor_df[useful_col]

    data = pd.merge(ff_factor_df, stock_return_series.to_frame(name='stock_return'), right_index=True,
                    left_index=True, how='inner')
    trading_days = data.index

    if data.empty or trading_days[-1] < event_date:
        return np.nan, 'Not enough data'
    event_trading_date = trading_days[trading_days >= event_date][0]
    post_event_days = trading_days[trading_days > event_trading_date]
    before_event_days = trading_days[trading_days < event_trading_date]

    if len(before_event_days) < -period_start_days or len(post_event_days) < period_end_days:
        return np.nan, 'Not enough date to calculate'

    if len(before_event_days) <= 40:
        return np.nan, 'Not enough training data'

    elif len(before_event_days) < 210:
        training_data = data.loc[before_event_days[:-10]]

    else:
        training_data = data.loc[before_event_days[-210:-10]]

    def get_detail_date(index):
        if index < 0:
            return before_event_days[index]
        else:
            return post_event_days[index - 1]

    event_start_date = get_detail_date(period_start_days)
    event_end_date = get_detail_date(period_end_days)

    testing_data = data.loc[event_start_date:event_end_date, useful_col]
    olsmd = sm.OLS(training_data['stock_return'], training_data[useful_col])
    olsres = olsmd.fit()
    CAR = sum(data.loc[event_start_date:event_end_date, 'stock_return'] - olsres.predict(testing_data))
    return CAR, 'Calculation Succeed'
