import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy import log

class DemoSpider(scrapy.Spider):
    name = "kempashop"
    login_page = "https://shop.uhlsportcompany.com/uhlsport/b2b/init.do?language=en&shop=1040_UK"
    urls_to_parse = ["https://shop.uhlsportcompany.com/uhlsport/catalog/categorieInPath/(layout=6_4_6_1&uiarea=1)/.do?key=0/0000000015/0000000061"]

    def start_requests(self):
        # Start by logging in
        return [FormRequest(self.login_page, formdata={'UserId': '101229551', 'password': 'call77'}, callback=self.after_login)]

    def after_login(self, response):
        self.log('Login Successful. Parsing all other URLs')
        # Here we get ALL Ids from kempa store and generate the urls
        for url in self.urls_to_parse:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        print response.body
        print "-------------------- REQUEST ------------------------------------------------------"
