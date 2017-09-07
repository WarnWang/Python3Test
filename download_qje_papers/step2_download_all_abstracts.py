#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step2_download_all_abstracts
# @Date: 7/9/2017
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os

import pandas as pd
from selenium import webdriver

from download_qje_papers.constants import *

df = pd.read_pickle(os.path.join('data', 'qje_paper_list.pkl'))

driver = webdriver.Chrome('/Users/warn/PycharmProjects/Python3Test/download_qje_papers/chromedriver')

for i in df.index:
    url = df.loc[i, URL]
    driver.get(url)

    abstract = driver.find_elements_by_class_name('abstract')
    if abstract:
        df.loc[i, ABSTRACT] = abstract[0].text

driver.close()

df.to_pickle(os.path.join('data', '20170907_qje_paper_add_abstract.pkl'))
df.to_excel(os.path.join('data', '20170907_qje_paper_add_abstract.xlsx'), index=False)
