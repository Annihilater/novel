#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/11/23 18:09
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : 1.py
import re

urls = ['https://www.biquge.com.cn/book/36760/',
        'https://www.biquge.com.cn/book/36760/62765.html',
        'https://www.biquge.com.cn/xiuzhen/']
for url in urls:
    if re.match('^https://www.biquge.com.cn/book/(\d*)/$', url):
        print('小说 ', url)
    if re.match('^https://www.biquge.com.cn/book/(\d*)/(\d*).html$', url):
        print('章节 ', url)
    if re.match('^https://www.biquge.com.cn/(.*)/$', url):
        print('专栏 ', url)
    if re.match('^/\w{1,}/$', url):  # 匹配专栏网址
        _url = 'https://www.biquge.com.cn/' + url
