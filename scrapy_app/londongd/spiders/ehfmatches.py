import datetime
import urlparse
import socket
import scrapy
from londongd.items import EhfmatchItem
from scrapy.loader import ItemLoader

class EhfmatchesSpider(scrapy.Spider):
    name = 'ehfmatches'
    start_urls = ['http://www.ehftv.com/gb/livestream-schedule']
    custom_settings = {
        'ITEM_PIPELINES': {
            'londongd.pipelines.EhfmatchPipeline':100
        }
    }

    def parse(self, response):

        items = []

        for li in response.css('ul.listview > li'):
        	date_1 = li.css('h2::text').extract_first()        
        	datetime_object = datetime.datetime.strptime(date_1, "%A, %d.%m.%Y")
        	datetime_object2 = datetime_object.strftime('%Y-%m-%d %H:%M:%S')
        	print "-----------------||||-------------"
        	print datetime_object2

        	for li2 in li.css('ul > li'):

	    	 	item = EhfmatchItem()

	        	img = li2.css("img").xpath("@src")
	        	imageURL = img.extract_first()

	        	link = li2.css('a::attr(href)').extract_first()
	        	title = li2.css('h4::text').extract_first()   
	        	time = li2.css('h5::text').extract_first()
	        	teams = li2.css('h3::text').extract_first()
	        	
	        	item['image'] = imageURL
	        	item['link'] = link
	        	item['title'] = title
	        	item['datetime_object'] = datetime_object2
	        	item['time'] = time
	        	item['teams'] = teams

        		items.append(item)

    	return items
