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
    allowed_domains = ["groups.google.com","accounts.google.com"]
    start_urls = ['https://accounts.google.com/signin/v2/identifier']

    allowed_domains = ['groups.google.com']
    login_page = 'https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=Identifier'
    start_urls = ['https://groups.google.com/forum/#!forum/lgdallmixed']


    def init_request(self):
        """This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        """Generate a login request."""
        return FormRequest.from_response(response,
                    formdata={'email': 'miguelpuig@gmail.com'},
                    callback=self.log_password)

	def log_password(self, response):
	    """
	    Enter the password to complete the log in.
	    """
	    return scrapy.FormRequest.from_response(
	        response,
	        formdata={'Passwd': self.var.password},
	        callback=self.check_login_response)
    	

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        if "Hi Herman" in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin..
            self.initialized()
        else:
            self.log("Bad times :(")
            # Something went wrong, we couldn't log in, so nothing happens.

    def parse_item(self, response):
    	print response
        # Scrape data from page