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
from scrapy.conf import settings
from londongd.items import SporteasyItem
from scrapy.conf import settings

import MySQLdb

class SizeClass(object):
    pass
    
class MyEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__    

class SporteasySpider(scrapy.Spider):
    name = "sporteasy"
    allowed_domains = ["sporteasy.net"]
    mainUrl = 'https://shop.uhlsportcompany.com'
    main_domain_prod = "https://london-gd-ladies-2nd-team.sporteasy.net"
    db = MySQLdb.connect(host="localhost",user=settings.get('MYSQL_USER'),passwd=settings.get('MYSQL_PASSWORD'),db=settings.get('MYSQL_DB'))
    custom_settings = {
        'ITEM_PIPELINES': {
            'londongd.pipelines.SporteasyPipeline':100
        }
    }    
    start_urls = ['https://www.sporteasy.net/en/login/']
    seasy_urls = ['https://london-gd-ladies-1st-team.sporteasy.net','https://london-gd-ladies-2nd-team.sporteasy.net']
    id_products = []
    item_stocks = []
    limit = ''
    
    def __init__(self, limit='', *args, **kwargs):
        
        super(SporteasySpider, self).__init__(*args, **kwargs)
        
        
		    
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
            formdata={'username': 'miguelpuig@gmail.com', 'password': 'Callthelaw77'},           
            callback=self.getUrls
        )
        
    def getUrls(self,response):
	    print "HOLA!"
	    for urlTeam in self.seasy_urls:
	    	if "ladies-1st" in urlTeam:
	    		team = 'W1'
	    	if "ladies-2nd" in urlTeam:
	    		team = "W2"
	    	
	    	print "TEAM: "+team	
	    	yield Request(url=urlTeam+"/calendarlist/2017-2018/all/",meta={'urlTeam': urlTeam,'team':team},callback=self.loadSchedule)
    

    
    def loadSchedule(self, response):
        
        trs = response.selector.xpath("//table[@id='event_calendar']//tr")
        number = 0
        for tr in trs:        	
        	link = tr.css('td.date a::attr(href)').extract_first()
        	number = number + 1
        	if number == 4:
				break
        	if link:
				print link
				yield scrapy.Request(response.meta['urlTeam'] + link,meta={'team': response.meta['team']},callback=self.loadEventById)
				
			
			

    
    def loadEventById(self,response):
	    itemSporteasy = SporteasyItem()
	    
	    when = response.css('li.event-infos__announcement__about.when strong::text').extract_first()
	    where = response.css('div.where a::text').extract_first()
	    where_link = response.css('div.where a::attr(href)').extract_first()
	    idEvent = response.css('ol#attendee_list_registration::attr(data-event-id)').extract_first()
	    eventInfo = response.css('div.content table tr')
	    typeEvent = eventInfo[0].css('td small::text').extract_first()
	    typeName = eventInfo[1].css('td::text').extract_first()
		
	    when2 = self.cleanText(when)
	    if "PM" in when2:
	    	when3 = when2.split("PM")
	    	when3 = when3[0]+"PM"
	    	
		if "AM" in when2:
			when3 = when2.split("AM")
			when3 = when3[0]+"AM"

	    datetime_object = datetime.datetime.strptime(when3, "%a, %b %d, %Y at %I:%M %p")

	    outputAtendees = []
	    attendees = response.css('ol li')
	    for attendee in attendees:
			att_name = attendee.css('a.name::text').extract_first()
			if att_name:
				outputAtendees.append(self.cleanText(att_name))
			

	    itemSporteasy['itemEventid'] = idEvent
	    itemSporteasy['itemTeam'] = response.meta['team']
	    itemSporteasy['itemDate'] = datetime_object
	    itemSporteasy['itemType'] = self.cleanText(typeEvent)
	    itemSporteasy['itemAttendees'] = outputAtendees
	    itemSporteasy['itemLocation'] = where
	    itemSporteasy['itemLocationLink'] = where_link
	    itemSporteasy['itemName'] = self.cleanText(typeName)
	    
	    
	    yield itemSporteasy
		
		
		
		