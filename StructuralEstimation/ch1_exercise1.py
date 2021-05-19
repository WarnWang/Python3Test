#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: ch1_exercise1
# @Date: 2021/5/1
# @Author: Mark Wang
# @Email: markwang@connect.hku.hk

import os

import numpy as np
from tqdm import tqdm
import pandas as pd
from pandas import DataFrame

MC_bar = 100
FC = 100
beta_0 = 1
beta_1 = 1
gamma_2 = 1
market_size = list(range(1, 101))

if __name__ == '__main__':
    for s in tqdm(market_size):
        B = 1 / (beta_1 * s)
        q = np.sqrt(FC / (B + gamma_2 / 2))

