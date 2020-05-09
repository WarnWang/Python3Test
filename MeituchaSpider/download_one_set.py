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

from bs4 import BeautifulSoup

from .user_agents import my_user_agent
from .config_file import Configuration


def download_picture(img_url, save_name, header):
    res = requests.get(img_url, headers=header)

    with open(save_name, 'wb') as f:
        f.write(res.content)


def download_one_set(url):
    req = requests.get(url, headers={'user_agent': my_user_agent()})
    soup = BeautifulSoup(req.content, 'lxml')
    set_title = soup.title.text
    logging.debug('The title of this set: {}'.format(set_title))

    image_id = re.findall(r'\d+', url)[-1]

    save_dir = os.path.join(Configuration.save_path, image_id)
    logging.debug('Save path would be {}'.format(save_dir))
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    final_page_link = soup.find_all(class_='nxt')[-1].get('href')
    last_page_reg = requests.get('{}{}'.format(url, final_page_link), headers={'user_agent': my_user_agent()})

    last_page_soup = BeautifulSoup(last_page_reg.content, 'lxml')
    with open(os.path.join(save_dir, 'index.html'), 'w') as f:
        f.write(last_page_soup.text)

    last_img_url = last_page_soup.find(class_='content').find_all('img')[-1].get('src')

    img_id = re.findall(r'\d+', last_img_url)[-1]
    logging.debug('There are {} images in this set'.format(img_id))
    headers = {'user_agent': my_user_agent()}
    for i in range(1, int(img_id) + 1):
        img_url = last_img_url.replace(img_id, str(i))
        file_name = '{}_{}'.format(image_id, img_url.split('/')[-1])
        save_path = os.path.join(save_dir, file_name)
        logging.debug('Start to download picture {}'.format(i))
        try:
            download_picture(img_url, save_path, headers)
        except Exception as e:
            logging.error("cannot download picture {} as {}".format(i, e))
        else:
            logging.debug('Picture {} download successfully'.format(i))
        if i % 5 == 0:
            headers = {'user_agent': my_user_agent()}
            time.sleep(5)


if __name__ == '__main__':
    # id_list = [20910, 20920, 12411, 6006, 4812, 3889, 4004]
    id_list = [32718, 32623, 32721, 28045, 27598, 32719, 32626, 32703, 32598, 32517, 31271, 30195, 29085, 28063, 27447,
               27602, 27089, 26738, 24251, 32639, 32583, 32304, 11183, 14028]
    for id_info in id_list:
        url = 'https://www.meitucha.com/a/{}/'.format(id_info)
        print('Start to download {}'.format(id_info))
        download_one_set(url)
