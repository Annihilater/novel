# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class NovelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = Field()
    name = Field()
    author = Field()
    status = Field()
    update_time = Field()
    last_chapter = Field()


class ChapterItem(scrapy.Item):
    chapter_num = Field()
    title = Field()
    content = Field()
