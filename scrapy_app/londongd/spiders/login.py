import datetime
import urlparse
import socket

from scrapy.loader.processors import MapCompose, Join
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.http import FormRequest




class LoginSpider(CrawlSpider):
    name = 'login'
    allowed_domains = ["web"]

    custom_settings = {
        #'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
    }
    # Start with a login request
    def start_requests(self):
        return [
            FormRequest(
                "https://www.sporteasy.net/en/login/",
                formdata={"user": "miguelpuig@gmail.com", "pass": "Callthelaw77"}
            )]

    def parse_item(self, response):
        print "hola"