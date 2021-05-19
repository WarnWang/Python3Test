#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: mimic_toni_markov
# @Date: 2021/5/19
# @Author: Mark Wang
# @Email: markwang@connect.hku.hk

import numpy as np

if __name__ == '__main__':
    rho = 0.5
    mu = 0.1421
    m = 2
    nz = 15
    f1 = np.zeros((nz, nz))
    f2 = np.ones((nz, nz))
    z = np.zeros(nz)

    s2 = 0.0081
    sig_z = np.sqrt(s2)
    sy = np.sqrt(s2 / (1 - rho ** 2))
    for i in range(nz):
        z[i] = -m * sy + ((2 * m * sy) / (nz - 1) * i)

    w = z[2] - z[1]
    for j in range(nz):
        for i in range(1, nz):
            minif = (z[i] - rho * z[j] - w / 2) / sig_z
            f1[i, j] = 0.5 * (1 + minif / np.sqrt(2))
            f2[i - 1, j] = 0.5 * (1 + minif / np.sqrt(2))

    z += mu
    f1 = f1.T
    f2 = f2.T
    trans = f2 - f1
    print(trans)
