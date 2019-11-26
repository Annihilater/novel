# -*- coding: utf-8 -*-
import re

import pymongo
import scrapy

from novel.items import ChapterItem, NovelItem
from novel.settings import MONGO_URI


class BiqugeSpider(scrapy.Spider):
    name = 'biquge'
    allowed_domains = ['www.biquge.com.cn']
    start_urls = ['https://www.biquge.com.cn/']
    boards = set()  # 存放已爬取的专栏网址

    def exists(self, name, title):
        client = pymongo.MongoClient(MONGO_URI)
        # collection = client[MONGO_DB]['ChapterItem']  # crawlab 配置
        col = client['novel']['ChapterItem']
        result = True if col.find_one({'name': name, 'title': title}) else False
        client.close()
        return result

    def parse(self, response):
        urls = response.css('a::attr(href)').extract()
        for url in urls:
            if re.match('^https://www.biquge.com.cn/book/(\d*)/$', url):  # 匹配小说网址
                yield scrapy.Request(url, callback=self.parse_book)
            if re.match('^/\w{1,}/$', url):  # 匹配专栏网址
                _url = 'https://www.biquge.com.cn/' + url
                if _url not in self.boards:  # 针对不在集合中的专栏网址进行爬取
                    self.boards.add(_url)
                    yield scrapy.Request(_url, callback=self.parse)

    def parse_book(self, response):
        """
        1. 提取小说简介信息返回 NovelItem
        2。 爬取未爬取的章节
        :param response:
        :return:
        """
        url = response.url
        name = response.css('#info h1::text').extract_first()
        author = response.css('#info p::text').re_first('作\xa0\xa0\xa0\xa0者：(.*)')
        status = response.css('#info p:nth-child(3)::text').re_first('状\xa0\xa0\xa0\xa0态：(.*)').replace(',', '')
        update_time = response.css('#info p:nth-child(4)::text').re_first('最后更新：(.*)')
        last_chapter = response.css('#info p:nth-child(5) a::text').extract_first()

        item = NovelItem()
        for field in item.fields:
            try:
                item[field] = eval(field)
            except NameError:
                self.logger.debug('Field is not Defined' + field)
        yield item

        base_url = 'https://www.biquge.com.cn'
        chapters = response.css('#list > dl > dd')
        for chapter in chapters:
            url = base_url + chapter.css('a::attr(href)').extract_first()
            title = chapter.css('a::text').extract_first().strip()
            if not self.exists(name, title):
                yield scrapy.Request(url, callback=self.parse_detail)
            else:
                self.logger.debug(f'已存在不保存  《{name}》  {title}')

        # 将未下载的小说章节存进 data 文件夹
        # dir = 'data/' + name + '/'
        # chapters = response.css('#list > dl > dd')
        # for chapter in chapters:
        #     url = base_url + chapter.css('a::attr(href)').extract_first()
        #     title = chapter.css('a::text').extract_first().strip()
        #     path = dir + title + '.txt'
        #     if not os.path.exists(path):  # 下载未下载的章节
        #         yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        """
        提取章节信息，返回 ChapterItem
        :param response:
        :return:
        """
        # self.logger.debug('UserAgent:' + str(response.request.headers['User-Agent'])) # 输出 UA，检查是否随机
        name = response.css('.con_top a:nth-child(4)::text').extract_first().strip()
        title = response.css('.bookname h1::text').extract_first().strip()
        _content = response.css('#content::text').extract()
        content = ''
        for line in _content:
            content = content + line.replace('\xa0\xa0\xa0\xa0', '')  # 除去特殊字符

        item = ChapterItem()
        for field in item.fields:
            try:
                item[field] = eval(field)
            except NameError:
                self.logger.debug('Field is not Defined' + field)
        yield item

        # 小说章节数据存进 data 文件夹
        # self.logger.debug('章节名称: ' + title)
        # dir = 'data/' + name + '/'
        # path = dir + title + '.txt'
        # if not os.path.exists(dir):
        #     os.mkdir(dir)
        #
        # if not os.path.exists(path):
        #     with open(path, 'x') as f:
        #         for text in content:
        #             text.replace('\xa0\xa0\xa0\xa0', '')  # 除去特殊字符
        #             f.write(text + '\n')
        #
        # # 点击下一章
        # next = 'https://www.biquge.com.cn' + response.css('.bottem1 a:nth-child(3)::attr(href)').extract_first()
        # if next.endswith('.html'):
        #     yield scrapy.Request(url=next, callback=self.parse_detail)
