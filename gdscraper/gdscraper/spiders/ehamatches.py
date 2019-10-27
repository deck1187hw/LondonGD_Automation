# -*- coding: utf-8 -*-
import scrapy
import datetime
import scrapy

from gdscraper.items import ehamatchesItem


class EhamatchesSpider(scrapy.Spider):
    name = "ehamatches"
    allowed_domains = ["englandhandball.com"]
    start_urls = ["https://www.englandhandball.com/regional-development-league/regional-league-south-east/women"]
    teamsItem = []

    def __init__(self, user='', password='', *args, **kwargs):
        self.teamsItem = []

    def parse(self, response):
        leagueName = response.css('div.page-title div.container h1::text').extract_first()

        if "Regional League South East - women's" in leagueName:
            gamesLi = response.css('div.female .carousel-container ul li')
            self.parse_team(gamesLi, 4)

        if "Regional League South East C - men's" in leagueName:
            gamesLi = response.css('div.male .carousel-container ul li')
            self.parse_team(gamesLi, 5)

        if "Regional League South East B - men's" in leagueName:
            gamesLi = response.css('div.male .carousel-container ul li')
            self.parse_team(gamesLi, 3)

        if "Premier Handball League" in leagueName:
            gamesLi = response.css('div.male .carousel-container ul li')
            self.parse_team(gamesLi, 1)
            gamesLi = response.css('div.female .carousel-container ul li')
            self.parse_team(gamesLi, 2)

        return self.teamsItem

    def parse_team(self, team, itemId):

        for sel in team:
            for index, attribute in enumerate(sel.xpath('@*'), start=1):
                attribute_name = sel.xpath('name(@*[%d])' % index).extract_first()
                attribute_value = attribute.extract()
                if attribute_name == "data-group":
                    tmpAttr = attribute_value.split("-")
                    date_year = tmpAttr[0]
                    date_fullmonth = tmpAttr[1]

            item = ehamatchesItem()
            venue = sel.css('.venue span::text').extract_first()
            team1 = sel.css('.team-1::text').extract_first()
            team2 = sel.css('.team-2::text').extract_first()

            fixture_block = sel.css('.fixture-block::text').extract()
            tmpfixture_block = fixture_block[1].replace(" ", "")
            tmpfixture_block2 = tmpfixture_block.split("@")

            date_day_num = sel.css('.fixture-block span.date::text').extract_first()
            date_day_week = tmpfixture_block2[0]
            date_day_time = tmpfixture_block2[1]
            date_month = sel.css('.fixture-block span.date span::text').extract_first()

            dateTmp = date_year + "-" + date_month + "-" + date_day_num + " " + date_day_time + ":00"
            dateTmp = dateTmp.replace('\n', '').replace('\r', '')
            datetime_object = datetime.datetime.strptime(dateTmp, '%Y-%b-%d %H:%M:%S')

            item['itemIsGD'] = 0
            if "London GD" in team1:
                item['itemIsGD'] = 1
            if "London GD" in team2:
                item['itemIsGD'] = 1

            item['itemType'] = itemId
            item['itemHome'] = team1
            item['itemAway'] = team2
            item['itemDate'] = datetime_object
            item['itemVenue'] = venue
            self.teamsItem.append(item)
