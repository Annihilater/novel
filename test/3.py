#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/11/26 11:33
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : 3.py
import pymongo

name = '道君1'
title = '第一章 没白来'
client = pymongo.MongoClient('127.0.0.1')
col = client['novel']['ChapterItem']
if False if col.find_one({'name': name, 'title': title}) else True:
    print('不存在')
else:
    print('存在')
client.close()
