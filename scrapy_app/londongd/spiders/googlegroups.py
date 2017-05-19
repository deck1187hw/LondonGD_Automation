# -*- coding: utf-8 -*-

import datetime
import urlparse
import socket

import scrapy
from londongd.items import LondongdItem
from scrapy.loader import ItemLoader
from scrapy.http import Request, FormRequest


class GooglegroupsSpider(scrapy.Spider):
    name = "googlegroups"
    login_page = "https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=Identifier"
    allowed_domains = ["https://accounts.google.com"]


    def parse(self, response):
    	print "LOGIN1"
        return scrapy.FormRequest('https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=Identifier',
                                     formdata={'email': 'miguelpuig@gmail.com'}, callback=self.log_password)

    def log_password(self, response):
    	print "LOGIN2"
    	return scrapy.FormRequest.from_response(
	        response,
	        formdata={'Passwd': '@Callthelaw88'},
	        callback=self.check_login_response)

    def check_login_response(self, response):
        print "TEST!!"