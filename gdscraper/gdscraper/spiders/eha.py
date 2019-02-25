# -*- coding: utf-8 -*-
import scrapy
import sys
import json
from json import JSONEncoder
import base64
from scrapy.http import FormRequest
from scrapy.http import Request
from gdscraper.items import Member

class EhaSpider(scrapy.Spider):
    name = "eha"
    allowed_domains = ["englandhandball.azolve.com"]
    start_urls = (
        'https://englandhandball.azolve.com/Account.mvc/Login',
    )
    azolveUser = ''
    azolvePass = ''
    azolveUserF = ''
    azolvePassF = ''
    items = []    

    def __init__(self, user='', password='', *args, **kwargs):
        
        self.azolveUser = user
        self.azolvePass = password
        self.items = []
						
    def parse(self, response):
	    if "user" in response.meta:
	    	self.azolveUserF = response.meta["user"]
	    	self.azolvePassF = response.meta["password"]
	    else:
        	self.azolveUserF = self.azolveUser
	    	self.azolvePassF = self.azolvePass	

	    params = {'userName': self.azolveUserF ,'password': self.azolvePassF, 'rememberMe': 'true'}
	    
	    yield FormRequest('https://englandhandball.azolve.com/Account.mvc/SecureWebLogIn', callback=self.loginAzolveStep2,method='POST', formdata=params)

    def loginAzolveStep2(self, response):
        boda = 'commands=[{"Id":1,"Service":"Repo","Method":"GetClubMembers","Arguments":[123728,"0","All+Members","Surname","asc",null,""]},{"Id":2,"Service":"Repo","Method":"GetClubMembersSummaryStatus","Arguments":[123728,"5",1,null,""]},{"Id":3,"Service":"Repo","Method":"SelectTransferCount","Arguments":[123728]}]'
        
        yield Request(url="https://englandhandball.azolve.com/WidgetService.mvc/ExecuteWidgetCommand", method="POST", body=boda, headers={'Content-Type':'application/json', 'User-Agent':'Mozilla/5.0'}, callback=self.loginAzolveStep3)
    
    def loginAzolveStep3(self, response):
	    jsonresponse = json.loads(response.body_as_unicode())
	    for member in jsonresponse[0]["Result"]["clubMembers"]:
	    	item = Member()
	    	item['MID'] = member['MID']
	    	item['Role'] = member['Role']
	    	item['UserId'] = member['UserId']
	    	item['FirstName'] = member['FirstName']
	    	item['Surname'] = member['Surname']
	    	item['EmailAddress'] = member['EmailAddress']
	    	item['Gender'] = member['Gender']
	    	item['MemberStateName'] = member['MemberStateName']
	    	item['MemberStateId'] = member['MemberStateId']
	    	item['CurrentStateId'] = member['CurrentStateId']
	    	item['ClubMemberDocId'] = member['ClubMemberDocId']
	    	item['MemberDocId'] = member['MemberDocId']
	    	self.items.append(item)
	    return self.items