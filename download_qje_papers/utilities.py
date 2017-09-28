#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: utilities
# @Date: 28/9/2017
# @Author: Mark Wang
# @Email: wangyouan@gamil.com


def switch_to_non_default_handle(driver):
    driver.close()
    driver.switch_to_window(driver.window_handles[0])
