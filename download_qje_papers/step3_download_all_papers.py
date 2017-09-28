#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step3_download_all_papers
# @Date: 28/9/2017
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os
import requests

from selenium import webdriver

from download_qje_papers.utilities import switch_to_non_default_handle

driver = webdriver.Chrome('/Users/warn/PycharmProjects/Python3Test/download_qje_papers/chromedriver')

lib_url = 'http://lib.hku.hk/'

login_button = '//*[@id="body_container"]/div[2]/div[1]/div/a'

driver.get(lib_url)

driver.find_element_by_xpath(login_button).click()
switch_to_non_default_handle(driver)

driver.find_element_by_name('userid').send_keys('markwang')
driver.find_element_by_name('password').send_keys('az1212AZ1212')

