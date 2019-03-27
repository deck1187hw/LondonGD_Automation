# -*- coding: utf-8 -*-
import scrapy
from gdscraper.items import kempaStoreItem


class KempaSpider(scrapy.Spider):
    name = "kempa"
    allowed_domains = ["kempa-sports.com"]
    start_urls = []

    def cleanText(self,text):
        if text:
            textFormatted = text.replace('\n', '').replace('\r', '').strip()
            return textFormatted.strip()
        else:
            return ''
            
    def start_requests(self):
        yield scrapy.Request(url='https://www.kempa-sports.com/en/start', callback=self.parseLinks)

    def parseLinks(self, response):
        for item in response.xpath('//*[@id="footer"]/div/div[1]/div[1]/ul/li'):
            link = item.css('a::attr(href)').extract_first()
            if link == '/en/products/category/110/shoes':  # remove this shit
                yield scrapy.Request(url='https://www.kempa-sports.com' + link, callback=self.parseCategory)

    def parseCategory(self, response):
        for item in response.xpath('//*[@id="productlist"]/li'):
            link = item.css('a::attr(href)').extract_first()
            yield scrapy.Request(url='https://www.kempa-sports.com' + link, callback=self.parseProduct)

    def parseProduct(self, response):
        itemKempa = kempaStoreItem()
        itemKempa['itemTitle'] = response.xpath('//*[@id="contentheader"]/h1/text()').extract_first()
        itemKempa['itemAllDescription'] = response.xpath('//*[@id="contentwrap"]/div/div[3]/p/text()').extract_first()
        itemKempa['itemId'] = response.xpath('//*[@id="contentheader"]/h2/text()').extract_first().replace('Art. ', '')
        itemKempa['itemInfoSizes'] = response.xpath('//*[@id="contentwrap"]/div/div[3]/div[2]/div/div/text()').extract_first()
        
        
        print itemKempa
