# -*- coding: utf-8 -*-
import scrapy


class KempaSpider(scrapy.Spider):
    name = "kempa"
    allowed_domains = ["kempa-sports.com"]
    start_urls = ['http://kempa-sports.com/']

    def parse(self, response):
    	print response.body
        pass
