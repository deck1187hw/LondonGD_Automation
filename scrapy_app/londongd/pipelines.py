# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

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
        db[settings['KEMPA_COLLECTION_ITEMS']].delete_many({})
        self.collection = db[settings['KEMPA_COLLECTION_ITEMS']]



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
class KempacatPipeline(object):

    def __init__(self):
        print "KEMPA CAT PIPELINE---------------------------------------"
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        db[settings['KEMPA_COLLECTION_CATS']].delete_many({})
        self.collection = db[settings['KEMPA_COLLECTION_CATS']]



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