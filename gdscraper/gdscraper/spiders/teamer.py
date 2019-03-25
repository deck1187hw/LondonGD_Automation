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
        eventList = response.xpath('//*[contains(@class,\'content_box\')]/div')
        for item in eventList:
        	tit = item.xpath('.//h3/a/b//text()').extract_first()
        	if tit is not None and "Training" in tit:
	        	itemSporteasy = SporteasyItem() 	
	        	itemSporteasy['itemLocation'] = item.xpath('.//table/tr[1]/td[2]//text()').extract()
	        	itemSporteasy['itemDate'] = item.xpath('.//table/tr[2]/td[2]//text()').extract()
	        	print tit