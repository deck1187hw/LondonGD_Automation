# -*- coding: utf-8 -*-
import scrapy
from gdscraper.items import EhafixturesItem


class EhafixturesSpider(scrapy.Spider):
    name = 'ehafixtures'
    allowed_domains = ['englandhandball.com']
    start_urls = ['https://www.englandhandball.com/league/premier-handball-league']
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

        leagueName = response.css('div.page-title div.container h1::text').extract_first()

        # Only for PHL Women take the 2nd
        if self.typeF == "women" and "premier" in response.request.url:
            leagueHtml = response.selector.xpath('//*[@id="standings"]/div[2]/div[2]').get()
            leagueName = response.selector.xpath('//*[@id="standings"]/div[2]/div[1]/p').get()
        else:
            leagueHtml = response.selector.xpath('//*[@id="standings"]/div[1]/div[2]').get()
            leagueName = response.selector.xpath('//*[@id="standings"]/div[1]/div[1]/p').get()

        item = EhafixturesItem()
        item['itemNameLeague'] = leagueName
        item['itemHtml'] = leagueHtml
        item['itemTeamId'] = self.teamIdF
        return item
