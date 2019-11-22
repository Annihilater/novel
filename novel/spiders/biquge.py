# -*- coding: utf-8 -*-
import os

import scrapy

from novel.items import NovelItem


class BiqugeSpider(scrapy.Spider):
    name = 'biquge'
    allowed_domains = ['www.biquge.com.cn']
    # start_urls = ['https://www.biquge.com.cn/']
    start_urls = ['https://www.biquge.com.cn/book/20672/']

    def parse(self, response):
        base_url = 'https://www.biquge.com.cn'
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

        url = base_url + response.css('#list dl dd:nth-child(2) a::attr(href)').extract_first()  # 第一章的 url
        # chapters = response.css('#list > dl > dd')
        # for chapter in chapters:
        #     url = base_url + chapter.css('a::attr(href)').extract_first()
        yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        title = response.css('.bookname h1::text').extract_first().strip()
        print(title)
        content = response.css('#content::text').extract()
        next = 'https://www.biquge.com.cn' + response.css('.bottem1 a:nth-child(3)::attr(href)').extract_first()

        path = 'data/不灭龙帝/' + title + '.txt'
        if not os.path.exists(path):
            with open(path, 'x') as f:
                for text in content:
                    text.replace('\xa0\xa0\xa0\xa0', '')
                    f.write(text)
                    f.write('\n')
            if next.endswith('.html'):
                yield scrapy.Request(url=next, callback=self.parse_detail)
