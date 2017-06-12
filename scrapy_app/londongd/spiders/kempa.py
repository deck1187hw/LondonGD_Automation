# -*- coding: utf-8 -*-
import scrapy
from londongd.items import KempaCatItem
from scrapy.loader import ItemLoader

class KempaSpider(scrapy.Spider):
    name = "kempa"
    allowed_domains = ["kempa-sports.com"]
    main_domain_prod = "http://www.kempa-sports.com"
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


        #GET CATEGORY URL
        itemCat['catUrl'] = response.url

        #GET CATEGORY SLUG
        itemCat['catSlug'] = itemCat['catUrl'].rsplit('/', 1)[-1]


        #GET CATEGORY ID
        itemCat['catId'] = itemCat['catUrl'].rsplit('/', 2)[-2]

        for link in response.css('ul#productlist li'):
            catHref = link.css('a::attr(href)').extract_first()

            #Get items
            #yield scrapy.Request(self.main_domain_prod + catHref,meta={'catid': catId, 'catslug':catSlug},callback=self.parse_item)

        self.catItems.append(itemCat)
        return itemCat


    def parse_item(self, response):

        #GET CAT ID FOR ARTICLE
        itemCatid = response.meta['catid']

        #GET CAT SLUG FOR ARTICLE
        itemCatslug = response.meta['catslug']
        print itemCatslug

        #GET ARTICLE TITLE
        itemTitle = response.css('h1[itemprop="name"]::text').extract_first()
        
        #GET ITEM URL
        itemURL = response.url

        #GET ARTICLE ID
        itemId = response.css('h2[itemprop="identifier"]::text').extract_first()
        itemId = itemId.replace('Art. ', '')

        # GET IMAGES
        itemImages = []
        imagesTmp = response.css('div.rightimages img').xpath('@src').extract()
        for itemImage in imagesTmp:
            if itemImage != '/content/images/spinner.gif':
                itemImage = itemImage.replace('ProductThumb', 'product')
                itemImages.append(itemImage)
        

        #GET ARTICLE DESCRIPTION
        itemAllDescription = response.css('.grid_6').extract_first()


        #GET ARTICLE INFO
        for info in response.css('div.info'):
            labelInfo = info.css('label::text').extract_first()
            valInfo = info.css('div.infoc').extract_first()

            if(labelInfo == 'Colors'):
                itemInfoColors = valInfo
            if(labelInfo == 'Technology'):
                itemInfoTechnology = valInfo
            if(labelInfo == 'Sizes'):
                itemInfoSizes = valInfo
            if(labelInfo == 'Available until'):
                itemInfoAvUntil = valInfo
        