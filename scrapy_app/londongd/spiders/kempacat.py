# -*- coding: utf-8 -*-
import scrapy
from londongd.items import KempaCatItem
from londongd.items import kempaStoreItem
from scrapy.loader import ItemLoader

class KempacatSpider(scrapy.Spider):
    name = "kempacat"
    allowed_domains = ["kempa-sports.com"]
    main_domain_prod = "http://www.kempa-sports.com"
    custom_settings = {
        'ITEM_PIPELINES': {
            'londongd.pipelines.KempacatPipeline':100
        }
    }
    start_urls = []
    catItems = []

    def __init__(self, filename=None):
        if filename:
            with open(filename, 'r') as f:
                for line in f.readlines():
                    self.start_urls.append(line.strip());
            f.close()


    def parse(self, response):

        itemCat = KempaCatItem()

        #GET CATEGORY TITLE
        itemCat['catTitle']  = response.css('h1::text').extract_first()
        
        #GET CATEGORY Image 
        itemCat['catImage'] = response.css('ul#productlist li img').xpath('@src').extract_first()

        #GET CATEGORY URL
        itemCat['catUrl'] = response.url

        #GET CATEGORY SLUG
        itemCat['catSlug'] = itemCat['catUrl'].rsplit('/', 1)[-1]


        #GET CATEGORY ID
        itemCat['catId'] = itemCat['catUrl'].rsplit('/', 2)[-2]

        self.catItems.append(itemCat)
        return itemCat