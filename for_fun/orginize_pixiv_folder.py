#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: orginize_pixiv_folder
# @Date: 2021/4/29
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import re
import os
import shutil

from tqdm import tqdm


ROOT_PATH = r'F:\Users\Pictures\pixiv'

if __name__ == '__main__':
    folder_info = os.listdir(ROOT_PATH)

    for dir_name in tqdm(folder_info):
        dir_path = os.path.join(ROOT_PATH, dir_name)
        if not os.path.isdir(dir_path):
            continue

        # get user id
        if dir_name.endswith(')'):
            user_id = re.findall(r'\d+', dir_name)[-1]
        elif '_' in dir_name:
            user_id = re.findall(r'\d+', dir_name)[0]
        else:
            continue

        new_dir_path = os.path.join(ROOT_PATH, user_id)
        if not os.path.isdir(new_dir_path):
            os.makedirs(new_dir_path)

        pic_names = os.listdir(dir_path)
        for f in pic_names:
            shutil.move(os.path.join(dir_path, f), os.path.join(new_dir_path, f))

        shutil.rmtree(dir_path)
