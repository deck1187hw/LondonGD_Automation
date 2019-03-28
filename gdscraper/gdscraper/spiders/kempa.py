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





