# Using Scrapy with Selenium to scape a rendered page [Updated]
from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from selenium import selenium

from linkedpy.items import LinkedPyItem


class LinkedPySpider(InitSpider):
    name = 'LinkedPy'
    allowed_domains = ['linkedin.com']
    login_page = 'https://www.linkedin.com/uas/login'
    start_urls = [
        "http://www.linkedin.com/csearch/results?type=companies&keywords=&pplSearchOrigin=GLHD&pageKey=member-home&search=Search#facets=pplSearchOrigin%3DFCTD%26keywords%3D%26search%3DSubmit%26facet_CS%3DC%26facet_I%3D80%26openFacets%3DJO%252CN%252CCS%252CNFR%252CF%252CCCR%252CI"]

    def __init__(self):
        InitSpider.__init__(self)
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*firefox", "http://www.linkedin.com")
        self.log("nnn Starting the Selenium Server! nnn")
        self.selenium.start()
        self.log("nnn Successfully, Started the Selenium Server! nnn")

    def __del__(self):
        self.selenium.stop()
        print
        self.verificationErrors
        CrawlSpider.__del__(self)

    def init_request(self):
        # """This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        # """Generate a login request."""
        return FormRequest.from_response(response,
                                         formdata={'session_key': 'email@address.com', 'session_password': 'password'},
                                         callback=self.check_login_response)

    def check_login_response(self, response):
        # """Check the response returned by a login request to see if we aresuccessfully logged in."""
        if "Sign Out" in response.body:
            self.log("nnnSuccessfully logged in. Let's start crawling!nnn")
            # Now the crawling can begin..
            return self.initialized()
        else:
            self.log("nnnFailed, Bad times :(nnn")
            # Something went wrong, we couldn't log in, so nothing happens.

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sel = self.selenium
        sel.open(response.url)
        time.sleep(2.5)
        sites = sel.select('//ol[@id='
        result - set
        ']/li')
        items = []
        for site in sites:
            item = LinkedPyItem()
            item['title'] = site.select('h2/a/text()').extract()
            item['link'] = site.select('h2/a/@href').extract()
            items.append(item)
        return items
