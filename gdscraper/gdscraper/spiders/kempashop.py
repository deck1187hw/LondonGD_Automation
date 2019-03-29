import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy import log
from json import JSONEncoder
import logging
import json
from gdscraper.items import StockItem

logger = logging.getLogger()

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class DemoSpider(scrapy.Spider):
    name = "kempashop"
    login_page = "https://shop.uhlsportcompany.com/uhlsport/b2b/init.do?language=en&shop=1040_UK"
    products = []
    start_urls = ["https://shop.uhlsportcompany.com/uhlsport/catalog/categorieInPath/(layout=6_4_6_1&uiarea=1)/.do?key=0/0000000015/0000000061"]

    def __init__(self, products='', *args, **kwargs):
	    #comming from CLI
        self.products  = products.split('|')

    def cleanText(self,text):
        if text:
            textFormatted = text.replace('\n', '').replace('\r', '').strip()
            return textFormatted.strip()
        else:
            return ''

    def parse(self, response):
	    logger.debug('Log message')
	    if "products" in response.meta:
	    	self.products = response.meta['products'].split('|')
            return [FormRequest(self.login_page, formdata={'UserId': '101229551', 'password': 'call77'}, callback=self.after_login)]


    def after_login(self, response):
        self.log('Login Successful. Parsing all other URLs')
        # Here we get ALL Ids from kempa store and generate the urls
        return Request(
            url="https://shop.uhlsportcompany.com/uhlsport/catalog/categorieInPath/(layout=6_4_6_1&uiarea=1)/.do?key=0/0000000015/0000000061",
            callback=self.fill_form_by_id)


    def fill_form_by_id(self, response):
        for productId in self.products:
            yield scrapy.FormRequest.from_response(
                    response,
                    formdata={'query': productId},
                    meta={'itemid': productId},
                    callback=self.load_product_id)


    def load_product_id(self, response):
        itemStock = StockItem()
        productTitle = response.css('.cat-prd-dsc span::text').extract_first()
        productId = response.css('.cat-prd-id p span div::text').extract_first()
        productSizes = response.selector.xpath("//table[@class='uhlGridTable']/tr[1]//th/text()").extract()
        productSizes_stock = response.selector.xpath("//table[@class='uhlGridItemPos']/tr[1]//td/text()").extract()
        productSizes_date = response.selector.xpath("//table[@class='uhlGridItemPos']/tr[2]//td/text()").extract()
        productSizes_stocklight = response.selector.xpath("//table[@class='uhlGridItemPos']/tr[3]//td//img/@src").extract()
        print "-------------------- REQUEST ------------------------------------------------------"

        finalSizes = self.clean_sizes(productSizes)
        finalSizes_lights_av = self.clean_stock_light(productSizes_stocklight)
        finalSizes_info_av = self.clean_product_sizes(productSizes_stock)
        finalSizes_date_av = self.clean_date_stock(productSizes_date)

        itemStock['id'] = self.cleanText(productId)
        itemStock['title'] = self.cleanText(productTitle)
        itemStock['sizes'] = MyEncoder().encode(finalSizes)
        itemStock['stock'] = MyEncoder().encode(finalSizes_info_av)
        itemStock['available'] = MyEncoder().encode(finalSizes_date_av)
        itemStock['light'] = MyEncoder().encode(finalSizes_lights_av)
        yield itemStock

    def clean_date_stock(self, productSizes_date):
        finalSizes_date_av = []
        for dateStock in productSizes_date:
            cleanSize = self.cleanText(dateStock)
            if cleanSize != '':
                finalSizes_date_av.append(cleanSize)
            else:
                finalSizes_date_av.append('-')
        return finalSizes_date_av


    def clean_product_sizes(self,productSizes_stock):
        finalSizes_info_av = []
        for info in productSizes_stock:
            cleanSize = self.cleanText(info)
            if cleanSize != '':
                finalSizes_info_av.append(cleanSize)
            else:
                finalSizes_info_av.append('-')
        return finalSizes_info_av

    def clean_stock_light(self, productSizes_stocklight):
        finalSizes_lights_av = []
        for light in productSizes_stocklight:
            if 'LIGHT_G_s.png' in light:
                finalSizes_lights_av.append('green')
            if 'LIGHT_Y_s.png' in light:
                finalSizes_lights_av.append('yellow')
            if 'LIGHT_R_s.png' in light:
                finalSizes_lights_av.append('red')
        return finalSizes_lights_av

    def clean_sizes(self, productSizes):
        finalSizes = []
        for size in productSizes:
            cleanSize = self.cleanText(size)
            if cleanSize != '':
                finalSizes.append(cleanSize)
        return finalSizes

