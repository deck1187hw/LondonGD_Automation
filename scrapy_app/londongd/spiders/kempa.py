# -*- coding: utf-8 -*-
# Run this like: scrapy crawl kempa -a filename=kempacats.txt
import scrapy
from londongd.items import KempaCatItem
from londongd.items import kempaStoreItem
from scrapy.loader import ItemLoader
from scrapy.selector import HtmlXPathSelector
from scrapy.conf import settings

class KempaSpider(scrapy.Spider):
    name = "kempa"
    allowed_domains = ["kempa-sports.com"]
    main_domain_prod = "http://www.kempa-sports.com"
    custom_settings = {
        'ITEM_PIPELINES': {
            'londongd.pipelines.KempaPipeline':100
        }
    }
    start_urls = []
    storeItems = []


    def __init__(self, filename=None):
        if filename:
            with open(filename, 'r') as f:
                for line in f.readlines():
                    self.start_urls.append(line.strip());
            f.close()


    def parse(self, response):


        #GET CATEGORY URL
        catUrl= response.url

        #GET CATEGORY SLUG
        catSlug = catUrl.rsplit('/', 1)[-1]


        #GET CATEGORY ID
        catid = catUrl.rsplit('/', 2)[-2]

        for link in response.css('ul#productlist li'):
            catHref = link.css('a::attr(href)').extract_first()

            #Get items
            yield scrapy.Request(self.main_domain_prod + catHref,meta={'catid': catid, 'catslug':catSlug},callback=self.parse_itemstore)



    def parse_itemstore(self, response):

        itemStore = kempaStoreItem()

        #GET CAT ID FOR ARTICLE
        itemStore['itemCatid'] = response.meta['catid']

        #GET CAT SLUG FOR ARTICLE
        itemStore['itemCatslug'] = response.meta['catslug']

        #GET ARTICLE TITLE
        itemStore['itemTitle'] = response.css('h1[itemprop="name"]::text').extract_first()
        
        #GET ITEM URL
        itemStore['itemURL'] = response.url

        #GET ARTICLE ID
        itemId = response.css('h2[itemprop="identifier"]::text').extract_first()
        itemStore['itemId']  = itemId.replace('Art. ', '')
        print "ItemID: "+itemStore['itemId']

        # GET IMAGES
        itemImages = []
        imagesTmp = response.css('div.rightimages img').xpath('@src').extract()
        for itemImage in imagesTmp:
            if itemImage != '/content/images/spinner.gif':
                itemImage = itemImage.replace('ProductThumb', 'product')
                if itemImage not in itemImages:                    
                    itemImages.append(itemImage)
        

        itemStore['itemImages'] = itemImages
        #GET ARTICLE DESCRIPTION
        itemStore['itemAllDescription']  = response.css('.grid_6').extract_first()
        
        
        #GET ARTICLE DESCRIPTION
        itemStore['itemDescription1']  = response.css('ul.material').extract_first()


        #GET ARTICLE INFO
        for info in response.css('div.info'):
            labelInfo = info.css('label::text').extract_first()
            valInfo = info.css('div.infoc::text').extract_first()
            valInfoHtml = info.css('div.infoc').extract_first()
            valInfoNew = info.css('div.infoc').extract_first()



            
            if(labelInfo == 'Colors'):
                itemStore['itemInfoColors'] = valInfo
                itemStore['itemNew'] = 0
                if 'New' in valInfoNew:
	            	itemStore['itemNew'] = 1
         
                
            if(labelInfo == 'Technology'):
                itemImages = []
                imagesTmp = info.css('div.infoc img').xpath('@src').extract()
                for itemImage in imagesTmp:
                    if itemImage not in itemImages:                    
                        itemImages.append(itemImage)


                itemStore['itemInfoTechnology'] = imagesTmp

            if(labelInfo == 'Sizes'):
            	vals = []
            	valInfo = info.css('div.infoc .sizeprice::text').extract()
            	for val in valInfo:
            		vals.append(val)
                itemStore['itemInfoSizes'] = vals
                
            if(labelInfo == 'Available until'):
                itemStore['itemInfoAvUntil'] = valInfo
                
            if(labelInfo == 'Available'):
                itemStore['itemInfoAvFrom'] = valInfo

        self.storeItems.append(itemStore)
        return itemStore
        