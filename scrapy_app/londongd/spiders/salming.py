# -*- coding: utf-8 -*-
import scrapy

from londongd.items import salmingStoreItem
from scrapy.loader import ItemLoader
from scrapy.selector import HtmlXPathSelector
import MySQLdb


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
		
		itemData = response.css('.product-data').extract_first()
		itemStore['itemData'] = itemData
		
		itemImages = response.css('.additional-images ul.bzoom a::attr(href)').extract()
		itemStore['itemImages'] = itemImages
		

		return itemStore
