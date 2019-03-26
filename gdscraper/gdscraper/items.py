# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GdscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Member(scrapy.Item):
	UserId = scrapy.Field()
	FirstName = scrapy.Field()
	Surname = scrapy.Field()
	EmailAddress = scrapy.Field()
	Gender = scrapy.Field()
	MemberStateName = scrapy.Field()
	MemberStateId = scrapy.Field()
	Role = scrapy.Field()
	CurrentStateId = scrapy.Field()
	ClubMemberDocId = scrapy.Field()
	MemberDocId = scrapy.Field()
	MID = scrapy.Field()
	
class ehamatchesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
	# Primary fields
	itemType = scrapy.Field()
	itemHome = scrapy.Field()
	itemAway = scrapy.Field()
	itemDate = scrapy.Field()
	itemIsGD = scrapy.Field()
	itemVenue = scrapy.Field()
	
	# Housekeeping fields
	url = scrapy.Field()
	project = scrapy.Field()
	spider = scrapy.Field()
	server = scrapy.Field()
	date = scrapy.Field()

class kempaStoreItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
	# Primary fields
	itemCatid = scrapy.Field()
	itemCatslug = scrapy.Field()
	itemTitle = scrapy.Field()
	itemNew = scrapy.Field()
	itemURL = scrapy.Field()
	itemId = scrapy.Field()
	itemAllDescription = scrapy.Field()
	itemInfoColors = scrapy.Field()
	itemInfoTechnology = scrapy.Field()
	itemInfoSizes = scrapy.Field()
	itemInfoAvUntil = scrapy.Field()
	itemImages = scrapy.Field()
	itemInfoAvFrom = scrapy.Field()
	itemDescription1 = scrapy.Field()
	
	
	# Housekeeping fields
	url = scrapy.Field()
	project = scrapy.Field()
	spider = scrapy.Field()
	server = scrapy.Field()
	date = scrapy.Field()	

class SporteasyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

	# Primary fields
	itemEventid = scrapy.Field()
	itemDate = scrapy.Field()
	itemName = scrapy.Field()
	itemType = scrapy.Field()
	itemAttendees = scrapy.Field()
	itemLocation = scrapy.Field()
	itemLocationLink = scrapy.Field()
	itemTeam = scrapy.Field()
	itemLinkEvent = scrapy.Field()


	# Housekeeping fields
	url = scrapy.Field()
	project = scrapy.Field()
	spider = scrapy.Field()
	server = scrapy.Field()
	date = scrapy.Field()

class EhafixturesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

	# Primary fields
	itemType = scrapy.Field()
	itemHtml = scrapy.Field()
	itemTeamId = scrapy.Field()
	itemNameLeague = scrapy.Field()


	# Housekeeping fields
	url = scrapy.Field()
	project = scrapy.Field()
	spider = scrapy.Field()
	server = scrapy.Field()
	date = scrapy.Field()


class SporteasyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
	# Primary fields
	itemEventid = scrapy.Field()
	itemDate = scrapy.Field()
	itemName = scrapy.Field()
	itemType = scrapy.Field()
	itemAttendees = scrapy.Field()
	itemLocation = scrapy.Field()
	itemLocationLink = scrapy.Field()
	itemTeam = scrapy.Field()
	itemLinkEvent = scrapy.Field()
	
	
	# Housekeeping fields
	url = scrapy.Field()
	project = scrapy.Field()
	spider = scrapy.Field()
	server = scrapy.Field()
	date = scrapy.Field()			
		