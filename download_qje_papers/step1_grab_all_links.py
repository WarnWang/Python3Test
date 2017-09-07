#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step1_grab_all_links
# @Date: 7/9/2017
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import datetime

import pandas as pd
from selenium import webdriver

url_prefix = 'https://academic.oup.com/qje/issue'

driver = webdriver.Chrome('/Users/warn/PycharmProjects/Python3Test/download_qje_papers/chromedriver')

YEAR = 'Year'
AUTHOR = 'Authors'
TITLE = 'Title'
ISSUE = 'Issue'
VOLUME = 'Volume'
URL = 'url'

columns = [YEAR, AUTHOR, TITLE, VOLUME, ISSUE, URL]

df = pd.DataFrame(columns=columns)

for i in range(125, 133):
    info_dict = {YEAR: 2010 + i - 125,
                 VOLUME: i}

    for j in range(1, 4 if i == 133 else 5):
        info_dict[ISSUE] = j
        print('{}, Start to handle volume {} issue {}'.format(datetime.date.today(), i, j))
        driver.get('{}/{}/{}'.format(url_prefix, i, j))

        articles = driver.find_elements_by_class_name('al-article-items')

        for article in articles:
            tmp_dict = info_dict.copy()
            tmp_dict[TITLE] = article.find_element_by_tag_name('a').text
            authors = article.find_elements_by_class_name('al-authors-list')
            if authors:
                tmp_dict[AUTHOR] = authors[0].text
            else:
                tmp_dict[AUTHOR] = None
            tmp_dict[URL] = article.find_element_by_class_name('ww-citation-primary').find_element_by_tag_name('a').text
            df.loc[df.shape[0]] = tmp_dict

df.loc[:, 'Journal'] = 'QJE'

driver.quit()

# df.to_csv('qje_paper_list.csv', index=False, sep='\t')
df.to_pickle('qje_paper_list.pkl')
