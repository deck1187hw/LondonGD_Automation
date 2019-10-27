# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import HtmlXPathSelector
from gdscraper.items import EhafixturesItem


class EhafixturesSpider(scrapy.Spider):
    name = 'ehafixtures'
    allowed_domains = ['englandhandball.com']
    start_urls = ['https://www.englandhandball.com/league/premier-handball-league'] # This is an example only for CLI
    type = ''
    teamId = ''
    typeF = ''
    teamIdF = ''

    def __init__(self, type='', teamId='', *args, **kwargs):
	    self.type = type
	    self.teamId = teamId

    def parse(self, response):
        if "teamId" in response.meta:
            self.typeF = response.meta["type"]
            self.teamIdF = response.meta["teamId"]
        else:
            self.typeF = self.type
            self.teamIdF = self.teamId
        
        item = EhafixturesItem()
        
        # Only for PHL Women take the 2nd
        if self.typeF == "women" and "premier" in response.request.url:
            #Women PHL only
            item['itemHtml'] = response.xpath('//*[@id="standings"]/div[2]/div[2]').extract_first()
            item['itemNameLeague'] = response.selector.xpath('//*[@id="standings"]/div[2]/div[1]/p').extract_first()
            item['itemTeamId'] = self.teamIdF

        else:
        	#Men and all
            item['itemHtml'] = response.xpath('//*[@id="standings"]/div[1]/div[2]').extract_first()
            item['itemNameLeague'] = response.selector.xpath('//*[@id="standings"]/div[1]/div[1]/p').extract_first()
            item['itemTeamId'] = self.teamIdF
        
        return item
