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


class EhfmatchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
	# Primary fields
	title = Field()
	link = Field()
	image = Field()
	datetime_object = Field()
	time = Field()
	teams = Field()
	
	# Housekeeping fields
	url = Field()
	project = Field()
	spider = Field()
	server = Field()
	date = Field()	
	
	
class StockItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
	# Primary fields
	title = Field()
	id = Field()
	sizes = Field()	
	available = Field()	
	stock = Field()	
	light = Field()		


class KempaCatItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
	# Primary fields
	catTitle = Field()
	catSlug = Field()
	catImage = Field()
	catUrl = Field()
	catId = Field()
	catImage = Field()
	
	# Housekeeping fields
	url = Field()
	project = Field()
	spider = Field()
	server = Field()
	date = Field()	

class kempaStoreItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
	# Primary fields
	itemCatid = Field()
	itemCatslug = Field()
	itemTitle = Field()
	itemURL = Field()
	itemId = Field()
	itemAllDescription = Field()
	itemInfoColors = Field()
	itemInfoTechnology = Field()
	itemInfoSizes = Field()
	itemInfoAvUntil = Field()
	itemImages = Field()
	itemInfoAvFrom = Field()
	itemDescription1 = Field()
	
	
	# Housekeeping fields
	url = Field()
	project = Field()
	spider = Field()
	server = Field()
	date = Field()
	
class salmingStoreItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
	# Primary fields
	itemDescription = Field()
	itemUrl = Field()
	itemData = Field()
	itemImages = Field()
	itemSizes = Field()
	itemImagemarketing = Field()
	itemTech = Field()
	
	
	# Housekeeping fields
	url = Field()
	project = Field()
	spider = Field()
	server = Field()
	date = Field()
	
class ehamatchesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
	# Primary fields
	itemType = Field()
	itemHome = Field()
	itemAway = Field()
	itemDate = Field()
	itemIsGD = Field()
	itemVenue = Field()
	
	# Housekeeping fields
	url = Field()
	project = Field()
	spider = Field()
	server = Field()
	date = Field()		
		