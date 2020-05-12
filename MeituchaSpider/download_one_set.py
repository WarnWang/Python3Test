#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: download_one_set
# @Date: 2020/5/9
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m MeituchaSpider.download_one_set
"""

import os
import re
import time
import logging
import requests

import pandas as pd
from pandas import DataFrame
from bs4 import BeautifulSoup

from MeituchaSpider.user_agents import my_user_agent
from MeituchaSpider.config_file import Configuration
from MeituchaSpider.scan_downloaded_file import query_set_info


def download_picture(img_url, save_name, header):
    res = requests.get(img_url, headers=header)

    with open(save_name, 'wb') as f:
        f.write(res.content)
    res.close()


def download_one_set(url):
    image_id = re.findall(r'\d+', url)[-1]
    database_info = pd.read_pickle(Configuration.database_path)
    image_info = database_info.loc[database_info['set_id'] == image_id]
    if image_info.empty:
        logging.debug('No download information, continue')
    else:
        image_row = image_info.iloc[0]
        if image_row['downloaded']:
            logging.debug('Image {} has been downloaded.'.format(image_id))
            return
        else:
            logging.debug('Image {} still need to be downloaded'.format(image_id))

    req = requests.get(url, headers={'user_agent': my_user_agent()})
    soup = BeautifulSoup(req.content, 'lxml')
    req.close()
    info_dict = query_set_info(soup, image_id)
    if image_info.empty:
        database_info: DataFrame = database_info.append(info_dict, ignore_index=True)
        database_info.to_pickle(Configuration.database_path)

    set_title = soup.title.text
    logging.debug('The title of this set: {}'.format(set_title))

    save_dir = os.path.join(Configuration.save_path, image_id)
    logging.debug('Save path would be {}'.format(save_dir))
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    total_page_num = info_dict['pic_num'] // 5
    if info_dict['pic_num'] % 5 != 0:
        total_page_num += 1

    for page_num in range(total_page_num):
        logging.debug('Start to download the images on page {}'.format(page_num))
        headers = {'user_agent': my_user_agent()}
        img_tags = soup.find('div', class_='content').find_all('img')

        for img_tag in img_tags:
            img_url = img_tag.get('src')
            file_name = '{}_{}'.format(image_id, img_url.split('/')[-1])
            save_path = os.path.join(save_dir, file_name)
            if os.path.isfile(save_path):
                continue
            try:
                download_picture(img_url, save_path, headers)
            except Exception as e:
                logging.error("cannot download picture {} as {}".format(file_name, e))
            else:
                logging.debug('Picture {} download successfully'.format(file_name))

        time.sleep(5)
        if page_num < total_page_num - 1:
            image_url = '{}?page={}'.format(url, page_num + 2)
            page_req = requests.get(image_url, headers=headers)
            soup = BeautifulSoup(page_req.content, 'lxml')
            page_req.close()

    database_info.loc[database_info['set_id'] == image_id, 'downloaded'] = True
    database_info.to_pickle(Configuration.database_path)
    logging.info('Set {} downloaded finished'.format(image_id))


if __name__ == '__main__':
    # id_list = [20910, 20920, 12411, 6006, 4812, 3889, 4004]
    # id_list = [32718, 32623, 32721, 28045, 27598, 32719, 32626, 32703, 32598, 32517, 31271, 30195, 29085, 28063, 27447,
    #            27602, 27089, 26738, 24251, 32639, 32583, 32304, 11183, 14028]
    # id_list = [32293, 32546]
    # id_list = [32586, 32660, 30249, 30251, 32617, 31900, 25303, 24051, 22189, 32702, 10766, 10714]
    id_list = [15040]
    for id_info in id_list:
        url = 'https://www.meitucha.com/a/{}/'.format(id_info)
        print('Start to download {}'.format(id_info))
        download_one_set(url)
