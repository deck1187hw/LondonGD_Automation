# -*- coding: utf-8 -*-
import scrapy


class EhanewsSpider(scrapy.Spider):
    name = "ehanews"
    allowed_domains = ["englandhandball.com"]
    start_urls = (
        'http://www.englandhandball.com/',
    )

    def parse(self, response):
        pass
