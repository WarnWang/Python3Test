#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

ROOT_PATH = '/mnt/d/wyatc/Documents/temp/MyFolder2'

if __name__ == '__main__':
    # Get the names of all sub folder
    dir_list = os.listdir(ROOT_PATH)

    result_str = list()
    # Go through all the folders
    for folder_name in dir_list:

        # Ignore folders which don't have total assets data
        if not folder_name.endswith('_total_assets'):
            continue

        company_name = folder_name[:-13]
        file_list = os.listdir(os.path.join(ROOT_PATH, folder_name))

        for f_name in file_list:
            if int(f_name[:-4]) < 2010:
                continue

            year = f_name[:-4]
            content = open(os.path.join(ROOT_PATH, folder_name, f_name))
            result_str.append('{} {}'.format(company_name, year))
            result_str.append(content.read())

    # save all result
    with open('/mnt/d/wyatc/Documents/temp/result.txt', 'w') as folder_name:
        folder_name.write('\n'.join(result_str))
