# -*- coding: utf-8 -*-
#CRAWL SINGLE ARTICLE: scrapy crawl kempastock -a artid="200209202"
import scrapy
import json
from json import JSONEncoder
import base64
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from scrapy.conf import settings
from londongd.items import StockItem
from scrapy.conf import settings

import MySQLdb

class SizeClass(object):
    pass
    
class MyEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__    

class KempastockSpider(scrapy.Spider):
    name = "kempastock"
    allowed_domains = ["shop.uhlsportcompany.com"]
    mainUrl = 'https://shop.uhlsportcompany.com'
    db = MySQLdb.connect(host="localhost",user=settings.get('MYSQL_USER'),passwd=settings.get('MYSQL_PASSWORD'),db=settings.get('MYSQL_DB'))
    custom_settings = {
        'ITEM_PIPELINES': {
            'londongd.pipelines.StockPipeline':100
        }
    }    
    start_urls = ['https://shop.uhlsportcompany.com/uhlsport/b2b/init.do?language=en&shop=1040_UK']
    id_products = []
    item_stocks = []
    limit = ''
    
    def __init__(self, limit='', artid='', *args, **kwargs):
        
        super(KempastockSpider, self).__init__(*args, **kwargs)
        print artid
        
        cur = self.db.cursor()
        
        if artid == '':
        	cur.execute("SELECT kempa_id FROM dwxf_store_products WHERE kempa_id <> '' LIMIT %s" % (limit))
        else:
        	cur.execute("SELECT kempa_id FROM dwxf_store_products WHERE kempa_id = %s LIMIT 1" % (artid))
        
        for row in cur.fetchall():
		    self.id_products.append(row[0]);
        self.db.close()
		    
    def cleanText(self,text):
        if text:
            textFormatted = text.replace('\n', '').replace('\r', '').strip()
            return textFormatted.strip()
        else:
            return ''
            
    def parse(self, response):
	    return scrapy.FormRequest.from_response(
            response,
            formdata={'UserId': '101229551', 'nolog_password': 'call77'},
            callback=self.loadKempaPageTree
        )
        
        
    def loadKempaPageTree(self, response):
        # check login succeed before going on
        return Request(url="https://shop.uhlsportcompany.com/uhlsport/catalog/categorieInPath/(layout=6_4_6_1&uiarea=1)/.do?key=0/0000000015/0000000061",
               callback=self.fillFormbyID)
        
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return
    
    def fillFormbyID(self, response):
        
        for id in self.id_products:
            
            
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'query': id},
                meta={'itemid': id},
                callback=self.loadProductByID
            )
        


    
    def loadProductByID(self,response):
        
        currentItem = response.meta.get('itemid')
        print currentItem
            
        areainfoNoItem = ''
        areainfoNoItem = response.css('.areainfo::text').extract_first()
        if areainfoNoItem:
            print "Item "+currentItem+" doesnt exist or cannot be found"
        else:        
            itemStock = StockItem()
            productTitle = response.css('.cat-prd-dsc span::text').extract_first()
            productId = response.css('.cat-prd-id p span div::text').extract_first()
            productSizes = response.selector.xpath("//table[@class='uhlGridTable']/tr[1]//th/text()").extract()
            productSizes_stock = response.selector.xpath("//table[@class='uhlGridItemPos']/tr[1]//td/text()").extract()  
            
            productSizes_date = response.selector.xpath("//table[@class='uhlGridItemPos']/tr[2]//td/text()").extract()
            productSizes_stocklight = response.selector.xpath("//table[@class='uhlGridItemPos']/tr[3]//td//img/@src").extract()  
            
            if not productTitle:
                print response.body
            
            self.id_products.remove(currentItem);
            
            finalSizes = []
            finalSizes_info_av = []
            finalSizes_date_av = []
            finalSizes_lights_av = []
            for size in productSizes:
                cleanSize=self.cleanText(size)
                if cleanSize!= '':
                    finalSizes.append(cleanSize)
            
            for light in productSizes_stocklight:
                if 'LIGHT_G_s.png' in light:
                    finalSizes_lights_av.append('green')
                if 'LIGHT_Y_s.png' in light:
                    finalSizes_lights_av.append('yellow')
                if 'LIGHT_R_s.png' in light:
                    finalSizes_lights_av.append('red') 
            
            for info in productSizes_stock:
                cleanSize=self.cleanText(info)
                if cleanSize != '':
                    finalSizes_info_av.append(cleanSize)
                else:
                    finalSizes_info_av.append('-')
                    
            for dateStock in productSizes_date:
                cleanSize=self.cleanText(dateStock)
                if cleanSize != '':                
                    finalSizes_date_av.append(cleanSize)
                else:
                    finalSizes_date_av.append('-')
                    
                    
            sizeObj = SizeClass()
            sizeObj.sizes = finalSizes
            sizeObj.finalSizes_info_av = finalSizes_info_av
            sizeObj.finalSizes_date_av = finalSizes_date_av
            sizeObj.finalSizes_lights_av = finalSizes_lights_av
            
                   
            itemStock['id'] = self.cleanText(productId)
            itemStock['title'] = self.cleanText(productTitle)
            itemStock['sizes'] = MyEncoder().encode(finalSizes) 
            itemStock['stock'] = MyEncoder().encode(finalSizes_info_av) 
            itemStock['available'] = MyEncoder().encode(finalSizes_date_av) 
            itemStock['light'] = MyEncoder().encode(finalSizes_lights_av) 
            yield itemStock
            #self.item_stocks.append(itemStock)
    