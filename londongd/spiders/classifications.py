# -*- coding: utf-8 -*-

import datetime
import urlparse
import socket

import scrapy
from londongd.items import LondongdItem
from scrapy.loader import ItemLoader


class ClassificationsSpider(scrapy.Spider):
    name = "classifications"
    allowed_domains = ["web"]
    start_urls = ['http://www.englandhandball.com/league/super-8-super-7']

    def parse(self, response):

		l = ItemLoader(item=LondongdItem(), response=response)
		# Load fields using XPath expressions
		l.add_xpath('title_w1', '//*[@id="standings"]//div[contains(@class, "league-table")][1]//p/text()')
		l.add_xpath('table_w1', '//*[@id="standings"]//div[contains(@class, "league-table")][1]//div[contains(@class, "table-responsive")][1]')
		
		l.add_xpath('title_m1', '//*[@id="standings"]//div[contains(@class, "league-table")][2]//p/text()')
		l.add_xpath('table_m1', '//*[@id="standings"]//div[contains(@class, "league-table")][2]//div[contains(@class, "table-responsive")][1]')

		# Housekeeping fields
		l.add_value('url', response.url)
		l.add_value('project', self.settings.get('BOT_NAME'))
		l.add_value('spider', self.name)
		l.add_value('server', socket.gethostname())
		l.add_value('date', datetime.datetime.now())
		
		return l.load_item()
