#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step01_prepare_regression_dataset
# @Date: 2020/9/16
# @Author: Mark Wang
# @Email: wangyouan@gamil.com


"""
python -m CAFR2020Disscussant.step01_prepare_regression_dataset
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame

from . import Constant as const


def get_fyear(datadate):
    month_day = datadate % 10000

    if month_day > 699:
        return datadate // 10000
    else:
        return datadate // 10000 - 1


if __name__ == '__main__':
    hf_temp_path = '/home/zigan/Documents/wangyouan/research/HedgeFundActivism/temp'
    kld_df: DataFrame = pd.read_pickle(os.path.join(hf_temp_path, '20181015_kld_csr_score.pkl'))
    ctat_df1: DataFrame = pd.read_csv(os.path.join(const.DATABASE_PATH, 'Compustat', '198901_199901_ctat_all_data.zip'),
                                      dtype={'cusip': 'str'})
    ctat_df2: DataFrame = pd.read_csv(os.path.join(const.DATABASE_PATH, 'Compustat', '199901_201906_ctat_all_data.zip'),
                                      dtype={'cusip': 'str'})
    ctat_df: DataFrame = pd.concat([ctat_df1, ctat_df2], ignore_index=True)
    ctat_df.loc[:, 'year'] = ctat_df['fyear'].fillna(ctat_df['datadate'].apply(get_fyear))
    ctat_df_valid: DataFrame = ctat_df.drop_duplicates(subset=['gvkey', 'year'], keep='last')

    ctat_df_valid.loc[:, 'cusip8'] = ctat_df_valid['cusip'].str[:-1]
    kld_with_ctat: DataFrame = kld_df.merge(ctat_df_valid.dropna(subset=['cusip', 'state'], how='any'),
                                            on=['cusip8', 'year'], how='inner')

    # Generate a UD state information
    state_list = kld_with_ctat['state'].drop_duplicates()
    year_list = kld_with_ctat['year'].drop_duplicates()

    ud_law_df = DataFrame(columns=['state', 'year', 'ud_law'])
    for state in state_list:
        tmp_df = DataFrame(columns=['year', 'ud_law'])
        ud_year = const.UD_LAW.get(state, 3000)
        for year in year_list:
            tmp_df.loc[tmp_df.shape[0], 'year'] = year

        tmp_df.loc[:, 'ud_law'] = (tmp_df['year'] >= ud_year).astype(int)
        tmp_df.loc[:, 'state'] = state
        ud_law_df: DataFrame = ud_law_df.append(tmp_df, ignore_index=True)

    kld_with_ctat_ud: DataFrame = kld_with_ctat.merge(ud_law_df, on=['state', 'year'])
    kld_with_ctat_ud.loc[:, 'at_ln'] = kld_with_ctat_ud['at'].apply(np.log)
    kld_with_ctat_ud.loc[:, 'roa'] = kld_with_ctat_ud['ni'] / kld_with_ctat_ud['at']
    kld_with_ctat_ud.loc[:, 'cash'] = kld_with_ctat_ud['che'] / kld_with_ctat_ud['at']
    kld_with_ctat_ud.loc[:, 'leverage'] = (kld_with_ctat_ud['dlc'] + kld_with_ctat_ud['dltt']) / kld_with_ctat_ud['at']
    kld_with_ctat_ud2: DataFrame = kld_with_ctat_ud.replace([np.inf, -np.inf], np.nan).drop(['do'], axis=1)
    kld_with_ctat_ud2.loc[:, 'year'] = kld_with_ctat_ud2['year'].astype(int)
    kld_with_ctat_ud2.to_stata(os.path.join(const.OUTPUT_PATH, '20200916_kld_ud_law_regression_data.dta'),
                               write_index=False)
