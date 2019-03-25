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
from gdscraper.items import SporteasyItem
from scrapy.conf import settings


class TrainingsSpider(scrapy.Spider):
    name = "trainings"
    allowed_domains = ["sporteasy.net"]
    start_urls = ['https://www.sporteasy.net/en/login/']
    seasy_urls = ['https://london-gd-ladies-1st-team.sporteasy.net','https://london-gd-ladies-2nd-team.sporteasy.net',"https://london-gd-1-1.sporteasy.net"]

    def __init__(self, limit='', *args, **kwargs):
        
        super(TrainingsSpider, self).__init__(*args, **kwargs)


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

	    for urlTeam in self.seasy_urls:
	    	partialUrl = "/calendarlist/2018-2019/all/"
	    	print urlTeam
	    	if "ladies-1st" in urlTeam:
	    		team = 2
	    	if "ladies-2nd" in urlTeam:
	    		team = 4
	    	if "gd-1-1" in urlTeam:
	    		team = 1
	    	if "beach-handball" in urlTeam:
	    		team = 10
	    		partialUrl = "/calendarlist/ebt-2017-18/all/"
	    	
			print partialUrl
	    	yield Request(url=urlTeam+partialUrl,meta={'urlTeam': urlTeam,'team':team},callback=self.loadSchedule)
    
    
    def loadSchedule(self, response):
        
        trs = response.selector.xpath("//table[@id='event_calendar']//tr")
        number = 0
        for tr in trs:        	
        	link = tr.css('td.date a::attr(href)').extract_first()
        	dtype = tr.css('td.icono a img::attr(data-tooltip)').extract_first()
        	for index, attribute in enumerate(tr.xpath('@*'), start=1):
        		attribute_name = tr.xpath('name(@*[%d])' % index).extract_first()
        		if attribute_name == 'class':
        			valueAttr = attribute.extract()
        			if valueAttr == 'next-event':
	        			if link:
							if dtype == 'Practice':
								yield scrapy.Request(response.meta['urlTeam'] + link,meta={'team': response.meta['team']},callback=self.loadEventById)

        	
    def loadEventById(self,response):
	    itemSporteasy = SporteasyItem()

		
	    when = response.css('li.event-infos__announcement__about.when strong::text').extract_first(default='')
	    where = response.css('div.where a::text').extract_first(default='')
	    where_link = response.css('div.where a::attr(href)').extract_first(default='')
	    idEvent = response.css('div#forum-guidelines::attr(data-event-team-id)').extract_first(default='')
	    eventInfo = response.css('div.content table tr')
	    
	    typeName = eventInfo[1].css('td::text').extract_first(default='')
	    cancelled = 0
	    if "scoreboard__details__is_cancelled" in response.body:
	    	cancelled = 1
	    	
	    	
	    typeEvent = 'Practice'
	    if '<td class="score"' in response.body:
	    	typeEvent = eventInfo[0].css('td small::text').extract_first(default='')
	    	
		
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
	    attributes = []
	    for attendee in attendees:
			for index, attribute in enumerate(attendee.xpath('@*'), start=1):
				attribute_name = attendee.xpath('name(@*[%d])' % index).extract_first()
				attributes.append((attribute_name, attribute.extract()))
				if attribute_name == 'data-attendance-group':
					valueAttr = attribute.extract()
					if valueAttr == 'available':
						att_name = attendee.css('a.name::text').extract_first(default='')
						if att_name:
							outputAtendees.append(self.cleanText(att_name))
						
			
									
		
	    itemSporteasy['itemEventid'] = idEvent
	    itemSporteasy['itemTeam'] = response.meta['team']
	    itemSporteasy['itemDate'] = datetime_object
	    itemSporteasy['itemType'] = self.cleanText(typeEvent)
	    itemSporteasy['itemAttendees'] = json.dumps(outputAtendees)
	    itemSporteasy['itemLocation'] = where
	    itemSporteasy['itemLocationLink'] = where_link
	    itemSporteasy['itemName'] = self.cleanText(typeName)
	    itemSporteasy['itemLinkEvent'] = response.url



	    if not cancelled:
	    	return itemSporteasy				    
        