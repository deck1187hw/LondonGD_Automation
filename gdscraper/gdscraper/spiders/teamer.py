# -*- coding: utf-8 -*-
import scrapy
import json
from json import JSONEncoder
import base64
import datetime
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from gdscraper.items import SporteasyItem


class TeamerSpider(scrapy.Spider):
    name = "teamer"
    allowed_domains = ["teamer.net"]
    start_urls = ['https://teamer.net/session/new']
    seasy_urls = ["https://teamer.net/teams/111660398-london-gd-2--3-men/events"]
    events = []

    def __init__(self, limit='', *args, **kwargs):
        
        super(TeamerSpider, self).__init__(*args, **kwargs)

    def cleanText(self,text):
        if text:
            textFormatted = text.replace('\n', '').replace('\r', '').strip()
            return textFormatted.strip()
        else:
            return ''

    def parse(self, response):
	    return scrapy.FormRequest.from_response(
            response,
            formnumber=1,
            formdata={'email': 'media@londongdhandball.co.uk', 'password': 'Callthelaw77'},           
            callback=self.getUrls
        )


    def getUrls(self,response):

	    for urlTeam in self.seasy_urls:
	    	print urlTeam
	    	yield Request(url=urlTeam,callback=self.loadSchedule)

    def loadSchedule(self, response):   
        for item in response.xpath('//*[contains(@class,\'content_box\')]/div'):
        	attributes = item.xpath('@*').extract()
        	id = 'NO'
        	for attr in attributes:
				print attr
				if "event_" in attr:
					id = attr
        	tit = item.xpath('.//h3/a/b//text()').extract_first()
        	if tit is not None and "Training" in tit:
	        	itemSporteasy = SporteasyItem() 	
	        	itemSporteasy['itemLocation'] = item.xpath('.//table/tr[1]/td[2]//text()').extract_first()
	        	when1 = item.xpath('.//table/tr[2]/td[2]//text()').extract_first()
	        	when2 = when1.split("@")
	        	when2[0] = self.cleanText(when2[0])
	        	when2[1] = self.cleanText(when2[1])
	        	when3 = when2[0]+' '+when2[1]
	        	itemSporteasy['itemDate'] = datetime.datetime.strptime(when3, "%a, %d %b, %Y  %I:%M%p")
	        	itemSporteasy['itemTeam'] = 3
	        	itemSporteasy['itemName'] = 'Training Men RDL'
	        	ids = id.split("_")	        
	        	itemSporteasy['itemEventid'] = ids[1]
	        	self.events.append(itemSporteasy)
    	return self.events