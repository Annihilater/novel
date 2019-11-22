#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/11/22 19:48
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : begin.py

from scrapy import cmdline

cmdline.execute('scrapy crawl biquge -s LOG_FILE=log/biquge.log'.split())
