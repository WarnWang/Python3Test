#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename: download_craft_data_from_fgowiki
# @Date: 31/3/2018
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os
import requests

from bs4 import BeautifulSoup
import pandas as pd

if __name__ == '__main__':
    root_path = '/home/zigan/Documents/wangyouan/for_fun/data_query_test'
    file_path = os.path.join(root_path, 'missing_craft_list.xlsx')

    df = pd.read_excel(file_path)

    if 'CN_name' not in df.keys():
        df.loc[:, 'CN_name'] = 1

    if 'JP_name' not in df.keys():
        df.loc[:, 'JP_name'] = 1

    base_url = 'https://fgowiki.com/guide/equipdetail/'

    percentage = 0

    for i in df.index:
        craft_id = df.loc[i, 'missing_id']
        if df.loc[i, 'CN_name'] != 1:
            continue

        web_content = requests.get('{}{}'.format(base_url, craft_id))
        s = web_content.content
        soup = BeautifulSoup(s, 'html.parser')
        name_list = soup.find_all(attrs={'name': 'keywords'})[0].get('content').split(',')
        df.loc[i, 'CN_name'] = name_list[0]
        df.loc[i, 'JP_name'] = name_list[1]

        if int(i * 100 / df.shape[0]) != percentage:
            percentage = int(i * 100 / df.shape[0])
            print(percentage, '% has been finished')

    df.to_excel(file_path, index=False)
