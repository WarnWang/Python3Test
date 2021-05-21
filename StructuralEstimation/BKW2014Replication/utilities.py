#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: utilities
# @Date: 2021/5/20
# @Author: Mark Wang
# @Email: markwang@connect.hku.hk

import numpy as np
from scipy.special import erf


def generate_profitability_distribution(mu, rho, sigma, number):
    f1 = np.zeros((number, number))
    f2 = np.ones((number, number))
    z = np.zeros(number)
    m = 2

    s2 = sigma ** 2
    sy = np.sqrt(s2 / (1 - rho ** 2))
    for i in range(number):
        z[i] = -m * sy + ((2 * m * sy) / (number - 1) * i)

    w = z[2] - z[1]
    for j in range(number):
        for i in range(1, number):
            minif = (z[i] - rho * z[j] - w / 2) / sigma
            f1[i, j] = 0.5 * (1 + erf(minif / np.sqrt(2)))
            f2[i - 1, j] = 0.5 * (1 + erf(minif / np.sqrt(2)))

    z += mu
    f1 = f1.T
    f2 = f2.T
    trans = f2 - f1
    return z, trans
