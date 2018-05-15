# -*- coding: utf-8 -*-
import scrapy
import json
from json import JSONEncoder
import base64
from scrapy.http import FormRequest
import sys
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from scrapy.conf import settings
from londongd.items import StockItem
from scrapy.conf import settings

import MySQLdb

class SizeClass(object):
    pass
    
class MyEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__    

class KempastockSpider(scrapy.Spider):
    name = "azolvemembers"
    allowed_domains = ["englandhandball.azolve.com"]
    mainUrl = 'https://englandhandball.azolve.com'
    db = MySQLdb.connect(host="localhost",user=settings.get('MYSQL_USER'),passwd=settings.get('MYSQL_PASSWORD'),db=settings.get('MYSQL_DB'))
    custom_settings = {
        'ITEM_PIPELINES': {
            'londongd.pipelines.StockPipeline':100
        }
    }    
    start_urls = ['https://englandhandball.azolve.com/Account.mvc/Login']
    azolveUser = ''
    azolvePass = ''  
    
    def __init__(self, azolveuser='', azolvepass='', *args, **kwargs):
        
        self.azolveUser = azolveuser
        self.azolvePass = azolvepass
        if not self.azolveUser:
			sys.exit("Write a user")
						
    def parse(self, response):
	    print self.azolveUser 
	    print 'logxin...'
	    params = {'userName': self.azolveUser,'password': 'king&country!', 'rememberMe': 'true'}
	    yield FormRequest('https://englandhandball.azolve.com/Account.mvc/SecureWebLogIn', callback=self.loginAzolveStep2,method='POST', formdata=params)
               
    def loginAzolveStep2(self, response):
        # check login succeed before going on
        print 'login2'
        print response.body
        boda = 'commands=[{"Id":1,"Service":"Repo","Method":"GetClubMembers","Arguments":[123728,"0","All+Members","Surname","asc",null,""]},{"Id":2,"Service":"Repo","Method":"GetClubMembersSummaryStatus","Arguments":[123728,"5",1,null,""]},{"Id":3,"Service":"Repo","Method":"SelectTransferCount","Arguments":[123728]}]'
        
        req1 = Request(url="https://englandhandball.azolve.com/WidgetService.mvc/ExecuteWidgetCommand", method="POST", body=boda, headers={'Content-Type':'application/json', 'User-Agent':'Mozilla/5.0'}, callback=self.loginAzolveStep3)
        print "aaa"
        yield req1
    
    def loginAzolveStep3(self, response):
	    print 'login3'
	    print response.body