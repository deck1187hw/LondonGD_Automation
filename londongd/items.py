# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class LondongdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
	# Primary fields
	title_w1 = Field()
	table_w1 = Field()
	title_m1 = Field()
	table_m1 = Field()	
	table = Field()

	
	# Housekeeping fields
	url = Field()
	project = Field()
	spider = Field()
	server = Field()
	date = Field()