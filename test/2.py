#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/11/26 10:31
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : 2.py
import pymongo

client = pymongo.MongoClient('127.0.0.1')
db = client['novel']
collection = db['NovelItem']
print(collection)
result = collection.find_one({'name': '天下'})
print(result)
