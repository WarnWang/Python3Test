#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: propensity_score_matching
# @Date: 12/11/2018
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import pandas as pd
from pscore_match.pscore import PropensityScore

# this list determines what variables would be used in PSM
cov_list = ['var1', 'var2']


def psm_match(original_df, treatment_df):
    treatment_df = treatment_df.dropna(subset=cov_list, how='any').reset_index(drop=True)
    treatment = treatment_df['id'].isin(original_df[id].apply(str)).apply(int)

    if treatment[treatment == 1].empty:
        use_cov_list = cov_list[:]
        use_cov_list.append('id')
        return pd.DataFrame(columns=use_cov_list)

    covariates = treatment_df[cov_list]
    pscore = pd.Series(PropensityScore(treatment, covariates).compute('probit'))
    columns = ['id', 'pscore']
    for i in range(5):
        columns.append(str(i))
        columns.append('{}_score'.format(i))

    result_df = pd.DataFrame(columns=columns)
    for i in treatment[treatment == 1].index:
        i_score = pscore[i]
        result_dict = {'id': str(int(treatment_df.loc[i, 'id'])),
                       'pscore': i_score}
        tmp_series = pscore[pscore.index != i]
        min_dis_index = (tmp_series - i_score).apply(abs).sort_values(ascending=True).head(5).index
        for j, k in enumerate(min_dis_index):
            result_dict[str(j)] = str(int(treatment_df.loc[k, 'id']))
            result_dict['{}_score'.format(j)] = pscore.loc[k]
        result_df.loc[result_df.shape[0]] = result_dict

    return result_df
