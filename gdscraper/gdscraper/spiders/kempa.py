# -*- coding: utf-8 -*-
import scrapy
from gdscraper.items import kempaStoreItem
from scrapy.http import Request, FormRequest


class KempaSpider(scrapy.Spider):
    name = "kempa"
    allowed_domains = ["kempa-sports.com", "shop.uhlsportcompany.com"]
    start_urls = []
    id_products = ['200849602', '200354120']
    products = []

    def cleanText(self,text):
        if text:
            textFormatted = text.replace('\n', '').replace('\r', '').strip()
            return textFormatted.strip()
        else:
            return ''

    def start_requests(self):
        yield scrapy.Request(url='https://www.kempa-sports.com/en/start', callback=self.parseLinks)

    def parseLinks(self, response):
        for item in response.xpath('//*[@id="footer"]/div/div[1]/div/ul/li'):
            link = item.css('a::attr(href)').extract_first()
            cat_name = item.css('a::text').extract_first()
            yield scrapy.Request(url='https://www.kempa-sports.com' + link, meta={'cat_name': cat_name, 'cat_slug': link}, callback=self.parseCategory)


    def parseCategory(self, response):
        for item in response.xpath('//*[@id="productlist"]/li'):
            link = item.css('a::attr(href)').extract_first()
            yield scrapy.Request(url='https://www.kempa-sports.com' + link, meta={'cat_name': response.meta['cat_name'], 'cat_slug': response.meta['cat_slug']}, callback=self.parseProduct)



    def parseProduct(self, response):
        itemKempa = kempaStoreItem()
        itemKempa['itemCatName'] = response.meta['cat_name']
        itemKempa['itemCatslug'] = response.meta['cat_slug']
        itemKempa['itemTitle'] = response.xpath('//*[@id="contentheader"]/h1/text()').extract_first()
        itemKempa['itemAllDescription'] = self.cleanText(response.xpath('//*[@id="contentwrap"]/div/div[3]/p/text()').extract_first())
        itemKempa['itemId'] = response.xpath('//*[@id="contentheader"]/h2/text()').extract_first().replace('Art. ', '')
        itemKempa['itemInfoSizes'] = self.cleanText(response.xpath('//*[@id="contentwrap"]/div/div[3]/div[2]/div/div/text()').extract_first())
        itemKempa['itemInfoColors'] = self.cleanText(response.xpath('//*[@id="contentwrap"]/div/div[3]/div[1]/div').extract_first())
        itemKempa['itemInfoTechnology'] = self.add_url_to_list_images(response.xpath('//*[@id="contentwrap"]/div/div[3]/div[3]/div//img/@src').extract())
        itemKempa['itemImages'] = self.add_url_to_list_images(response.xpath('//*[@class="mainimage"]/img/@src').extract())

        return itemKempa


    def add_url_to_list_images(self, imageList):
        for i in xrange(len(imageList)):
            if "spinner" not in imageList[i]:
                imageList[i] = "https://www.kempa-sports.com/"+imageList[i]
            else:
                del imageList[i]
        return imageList





