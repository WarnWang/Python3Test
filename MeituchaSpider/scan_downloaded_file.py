#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: scan_downloaded_file
# @Date: 2020/5/11
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m MeituchaSpider.scan_downloaded_file
"""

import os
import requests
import time
import re

import pandas as pd
from pandas import DataFrame
from bs4 import BeautifulSoup

from .config_file import Configuration
from .user_agents import my_user_agent


def query_set_info(set_soup):
    set_info_dict = {'set_id': set_id, 'downloaded': False, 'set_title': set_soup.title.text}

    info_tag = set_soup.find('div', class_='tuji')

    info_list = info_tag.find_all('p')
    institution_tag = info_list[0].find('a')
    set_info_dict['institution_name'] = institution_tag.text
    int_id = re.findall(r'\d+', institution_tag.get('href'))
    if int_id:
        set_info_dict['institution_id'] = int_id[0]

    set_info_dict['pic_num'] = int(re.findall(r'\d+', info_list[1].text)[0])
    model_tag = info_list[3].find('a')
    set_info_dict['model_name'] = model_tag.text
    model_id = re.findall(r'\d+', model_tag.get('href'))
    if model_id:
        set_info_dict['model_id'] = model_id[0]

    tag_list = set_soup.find('div', class_='fenxiang_l').find_all('a')
    tag_names = list()
    tag_ids = list()
    for tag_info in tag_list:
        tag_names.append(tag_info.text)
        tag_ids.append(tag_info.get('href').split('/')[-2])
    set_info_dict['tags_list'] = ' '.join(tag_names)
    set_info_dict['tag_id_list'] = '|'.join(tag_ids)
    return set_info_dict


if __name__ == '__main__':
    if os.path.isfile(Configuration.database_path):
        df: DataFrame = pd.read_pickle(Configuration.database_path)
    else:
        df = DataFrame(columns=['set_id', 'set_title', 'model_id', 'model_name', 'institution_name', 'institution_id',
                                'tags_list', 'tag_id_list', 'downloaded', 'pic_num'])

    for set_id in os.listdir(Configuration.save_path):
        if not os.path.isdir(os.path.join(Configuration.save_path, set_id)):
            continue
        if not df.loc[df['set_id'] == set_id].empty:
            continue

        print('Start to download set id {} information'.format(set_id))
        set_url = 'https://www.meitucha.com/a/{}/'.format(set_id)
        set_page_req = requests.get(set_url, headers={'user_agent': my_user_agent()})
        set_page_soup = BeautifulSoup(set_page_req.content, 'lxml')
        result_dict = query_set_info(set_page_soup)
        result_dict['downloaded'] = True

        df: DataFrame = df.append(result_dict, ignore_index=True)
        df.to_pickle(Configuration.database_path)
        print('Set id {} download finished'.format(set_id))
        time.sleep(5)
