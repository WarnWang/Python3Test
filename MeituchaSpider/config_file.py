#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: config
# @Date: 2020/5/9
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os

class Configuration(object):
    save_path = '/mnt/d/wyatc/photos/meitucha'
    database_path = os.path.join(save_path, 'saved_pic.pkl')
