#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: constants
# @Date: 2021/5/21
# @Author: Mark Wang
# @Email: markwang@connect.hku.hk

class PARAMETERS(object):
    ###########################################
    # Model initial parameters
    ###########################################
    lambda_ = 0.0906983393549567
    gamma_ = 11.0530988801549661
    delta_ = 0.0634630044682483
    mu_ = -2.2413654287674789
    rho_ = 0.5286754702975660
    sigma_ = 0.5457619195960740
    theta_ = 0.4177055908170345

    ###########################################
    # Constants
    ###########################################
    # risk-free rate
    RF = 0.02

    # corporate income tax
    TAU_C = 0.1
    BETA = 1 / (1 + RF * (1 + TAU_C))

    # define some grid parameters
    Z_NUM = 15
    P_NUM = 24
    P_NEXT_NUM = 64
    I_NUM = 61

    N_FIRMS = 93750
