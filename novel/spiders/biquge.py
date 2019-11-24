# -*- coding: utf-8 -*-
import os
import re

import scrapy

from novel.items import NovelItem


class BiqugeSpider(scrapy.Spider):
    name = 'biquge'
    allowed_domains = ['www.biquge.com.cn']
    # start_urls = ['https://www.biquge.com.cn/']
    start_urls = ['https://www.biquge.com.cn/']
    boards = set()  # 存放已爬取的专栏网址

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
        base_url = 'https://www.biquge.com.cn'
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

        dir = 'data/' + name + '/'
        chapters = response.css('#list > dl > dd')
        for chapter in chapters:
            url = base_url + chapter.css('a::attr(href)').extract_first()
            title = chapter.css('a::text').extract_first().strip()
            path = dir + title + '.txt'
            if not os.path.exists(path):  # 下载未下载的章节
                yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        # self.logger.debug('UserAgent:' + str(response.request.headers['User-Agent'])) # 输出 UA，检查是否随机
        name = response.css('.con_top a:nth-child(4)::text').extract_first().strip()
        title = response.css('.bookname h1::text').extract_first().strip()
        self.logger.debug('章节名称: ' + title)
        content = response.css('#content::text').extract()
        next = 'https://www.biquge.com.cn' + response.css('.bottem1 a:nth-child(3)::attr(href)').extract_first()
        dir = 'data/' + name + '/'
        path = dir + title + '.txt'
        if not os.path.exists(dir):
            os.mkdir(dir)

        if not os.path.exists(path):
            with open(path, 'x') as f:
                for text in content:
                    text.replace('\xa0\xa0\xa0\xa0', '')  # 除去特殊字符
                    f.write(text + '\n')

        if next.endswith('.html'):
            yield scrapy.Request(url=next, callback=self.parse_detail)
