#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: download_pictures_by_model_id
# @Date: 2020/5/10
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m MeituchaSpider.download_pictures_by_model_id
"""

import os
import re
import time
import logging
import requests

from bs4 import BeautifulSoup

from MeituchaSpider.user_agents import my_user_agent
from MeituchaSpider.download_one_set import download_one_set


def get_page_set_info(page_soup):
    set_box = page_soup.find(class_='hezi')
    li_list = set_box.find_all('li')
    model_url_list = list()
    for li_tag in li_list:
        model_url = 'https://www.meitucha.com{}'.format(li_tag.find('a').get('href'))
        model_url_list.append(model_url)

    return model_url_list

def get_all_model_set(model_id):
    model_page_url = 'https://www.meitucha.com/t/{}'.format(model_id)
    page_req = requests.get(model_page_url, headers={'user_agent': my_user_agent()})

    first_page_soup = BeautifulSoup(page_req.content, 'lxml')
    page_req.close()

    # Check if multiple page
    pagination_tag = first_page_soup.find(class_='pagination')
    set_url_list = get_page_set_info(first_page_soup)
    if pagination_tag is None:
        logging.debug('Model {} only has one page'.format(model_id))
    else:
        page_link = pagination_tag.find_all('li')
        last_page_index = int(page_link[-2].text)
        logging.debug('There are {} pages'.format(last_page_index))
        for i in range(2, last_page_index + 1):
            logging.debug('Start to download page {} set link'.format(i))
            page_url = '{}?page={}'.format(model_page_url, i)
            next_page_reg = requests.get(page_url, headers={'user_agent': my_user_agent()})
            page_soup = BeautifulSoup(next_page_reg.content, 'lxml')
            next_page_reg.close()
            set_url_list.extend(get_page_set_info(page_soup))
            time.sleep(5)

    logging.info('Model {} has {} sets.'.format(model_id, len(set_url_list)))
    for set_url in set_url_list:
        logging.debug('Start downloading {}'.format(set_url))
        download_one_set(set_url)
        logging.debug("Set downloaded finished.")
        time.sleep(1)

    logging.info('Model {} downloaded finished'.format(model_id))


if __name__ == '__main__':
    import sys

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    # for model_id in [945, 4044, 4348, 506, 799, 2265, 5482, 624, 289, 292]:
    # for model_id in [292, 3152, 943, 2172, 3172]:
    for model_id in [908, 943, 2172, 3172]:
        get_all_model_set(model_id)
