# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MatchreportItem(scrapy.Item):
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