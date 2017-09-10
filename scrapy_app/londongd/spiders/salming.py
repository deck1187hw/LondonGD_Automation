# -*- coding: utf-8 -*-
import scrapy

from londongd.items import salmingStoreItem
from scrapy.loader import ItemLoader
from scrapy.selector import HtmlXPathSelector
import MySQLdb
import json

class SizesClass(object):
    def __init__(self, sizeVal, sizeName ):
        self.sizeVal = sizeVal
        self.sizeName = sizeName
        
class SalmingSpider(scrapy.Spider):
    name = "salming"
    allowed_domains = ["salming.com"]
    main_domain_prod = "https://www.salming.com"
    db = MySQLdb.connect(host="localhost",user="londongd",passwd="@Callthelaw77",db="londongd_j3")
    custom_settings = {
        'ITEM_PIPELINES': {
            'londongd.pipelines.SalmingPipeline':100
        }
    }
    start_urls = []



    def __init__(self, filename=None):
		print "HOLA"
		# you must create a Cursor object. It will let
		#  you execute all the queries you need
		cur = self.db.cursor()
		
		# Use all the SQL you like
		cur.execute("SELECT * FROM dwxf_store_products_salming")
		
		# print all the first cell of all the rows
		for row in cur.fetchall():
		    self.start_urls.append(row[2]);
		self.db.close()


    def parse(self, response):
		
		itemStore = salmingStoreItem()
		itemStore['itemUrl'] = response.url
		
		#GET ITEM DESCRIPTION
		itemDescription = response.css('.uc-product-description').extract_first()
		itemStore['itemDescription'] = itemDescription
		
		#GET ITEM PRODUCT DATA
		itemData = response.css('.product-data').extract_first()
		itemStore['itemData'] = itemData
		
		
		#GET ITEM IMAGES
		itemImages = []
		itemImagesTmp = response.css('.additional-images ul.bzoom a::attr(href)').extract()
		for itemImage in itemImagesTmp:
			itemImages.append(itemImage)

		
		itemImages = ','.join(map(str, itemImages))
		itemStore['itemImages'] = itemImages

		
		sizesAll = []
		sizesTmp = response.css('.size-sku select#variant-sku option::text').extract()
		sizesTmpValue = response.css('.size-sku select#variant-sku option::attr(value)').extract()
		
		i = 0
		for sizeVal in sizesTmpValue:
			ob1 = sizeVal+'||'+sizesTmp[i]		
			sizesAll.append(ob1)

			i = i +1		
		
		
		itemStore['itemSizes'] = ','.join(map(str, sizesAll))

		
		#IMAGE MARKETING
		itemImagemarketing = response.css('.family-header img::attr(src)').extract_first()
		itemStore['itemImagemarketing'] = itemImagemarketing
		
		#TECH CONTAINER
		itemTech = response.css('.tech-container').extract_first()
		itemStore['itemTech'] = itemTech
		
		return itemStore
