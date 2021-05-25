#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: select_wallpaper
# @Date: 2021/4/29
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os
import shutil

from PIL import Image
from tqdm import tqdm

PIXIV_PATH = r'F:\Users\Pictures\pixiv'
TARGET_PATH = r'F:\Users\Pictures\wallpaper'

if __name__ == '__main__':
    dir_list = os.listdir(PIXIV_PATH)
    for dir_name in tqdm(dir_list):
        dir_path = os.path.join(PIXIV_PATH, dir_name)
        if not os.path.isdir(dir_path):
            continue

        for f in os.listdir(dir_path):
            if f.endswith('.png') or f.endswith('.jpg'):
                im = Image.open(os.path.join(dir_path, f))
                w, h = im.size
                if w < 1980 or h < 1080:
                    continue

                if 15 / 9 <= w / h <= 17 / 9:
                    shutil.copy(os.path.join(dir_path, f), os.path.join(TARGET_PATH, f))
