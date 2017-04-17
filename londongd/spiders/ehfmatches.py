import datetime
import urlparse
import socket
import scrapy
from londongd.items import EhfmatchItem
from scrapy.loader import ItemLoader

class EhfmatchesSpider(scrapy.Spider):
    name = 'ehfmatches'
    start_urls = ['http://www.ehftv.com/gb/livestream-calendar']

    def parse(self, response):

        items = []

        for li in response.css('ul.listview > li'):

    	 	item = EhfmatchItem()

        	img = li.css("img").xpath("@src")
        	imageURL = img.extract_first()

        	link = li.css('a::attr(href)').extract_first()
        	title = li.css('h4::text').extract_first()        	
        	date_1 = li.css('h2::text').extract_first()        
        	datetime_object = datetime.datetime.strptime(date_1, "%A, %d.%m.%Y").date()
        	time = li.css('h5::text').extract_first()
        	teams = li.css('h3::text').extract_first()

        	item['image'] = imageURL
        	item['link'] = link
        	item['title'] = title
        	item['datetime_object'] = date_1
        	item['time'] = time
        	item['teams'] = teams

        	items.append(item)

    	return items
