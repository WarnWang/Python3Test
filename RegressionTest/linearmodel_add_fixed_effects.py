#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename: linearmodel_add_fixed_effects
# @Date: 9/7/2018
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import numpy as np
from statsmodels.datasets import grunfeld
from linearmodels import PanelOLS

if __name__ == '__main__':
    data = grunfeld.load_pandas().data
    data.year = data.year.astype(np.int64)
    # MultiIndex, entity - time
    data = data.set_index(['firm', 'year'])
    mod = PanelOLS(data.invest, data[['value', 'capital']], entity_effects=True)
    res = mod.fit(cov_type='clustered', cluster_entity=True)

    print(res.summary)
