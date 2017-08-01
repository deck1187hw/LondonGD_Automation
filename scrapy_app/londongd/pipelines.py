# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import MySQLdb

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log



class EhfmatchPipeline(object):

    def __init__(self):
        print "EHF MATCHES PIPELINE---------------------------------------"
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        db[settings['MONGODB_EHFMATCHES_COLLECTION']].delete_many({})
        self.collection = db[settings['MONGODB_EHFMATCHES_COLLECTION']]


    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item

#for the items
class KempaPipeline(object):

    def __init__(self):
        print "KEMPA ITEM PIPELINE---------------------------------------"
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        #db[settings['KEMPA_COLLECTION_ITEMS']].delete_many({})
        self.collection = db[settings['KEMPA_COLLECTION_ITEMS']]



    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
        	self.collection.update({'itemId':item['itemId']},dict(item), upsert= True)
        	log.msg("Added to MongoDB database!",level=log.DEBUG, spider=spider)
        return item  
        
        
        
        
#for salming  items
class SalmingPipeline(object):

    def __init__(self):
        self.conn = MySQLdb.connect(
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            db=settings['MYSQL_DB'],
            host='localhost',
            charset="utf8",
            use_unicode=True
        )
        self.cursor = self.conn.cursor()



    def process_item(self, item, spider):
	    
        try:
            self.cursor.execute("""UPDATE dwxf_store_products_salming SET description=%s, product_data=%s, images=%s,sizes=%s,image_marketing=%s,techinfo=%s WHERE url_salming=%s""", (item['itemDescription'], item['itemData'], item['itemImages'], item['itemSizes'],item['itemImagemarketing'],item['itemTech'], item['itemUrl']))
            self.conn.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])

            return item    

#for the categories
class KempacatPipeline(object):

    def __init__(self):
        print "KEMPA CAT PIPELINE---------------------------------------"
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        #db[settings['KEMPA_COLLECTION_CATS']].delete_many({})
        self.collection = db[settings['KEMPA_COLLECTION_CATS']]



    def process_item(self, item, spider):
        valid = True

        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
        	self.collection.update({'catId':item['catId']},dict(item), upsert= True)
        	log.msg("Added to MongoDB database!",level=log.DEBUG, spider=spider)
            
        return item          