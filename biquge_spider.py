#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/11/22 19:48
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : biquge_spider.py

from scrapy import cmdline

cmdline.execute('scrapy crawl biquge'.split())
