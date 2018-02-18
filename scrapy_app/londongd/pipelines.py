# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import MySQLdb
import logging

from scrapy.conf import settings
from scrapy.exceptions import DropItem



class EhfmatchPipeline(object):

    def __init__(self):
        #print "EHF MATCHES PIPELINE---------------------------------------"
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
            logging.log("Added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item

#for the items
class KempaPipeline(object):

    def __init__(self):
        #print "KEMPA ITEM PIPELINE---------------------------------------"
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
        	logging.log("Added to MongoDB database!",level=log.DEBUG, spider=spider)
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


class StockPipeline(object):

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
        #self.cursor.execute("""TRUNCATE TABLE dwxf_store_products_stock""")
        #self.conn.commit()



    def process_item(self, item, spider):
		try:
						
			self.cursor.execute("""REPLACE INTO dwxf_store_products_stock (kempa_id,sizes,available,light,title,stock) VALUES (%s,%s,%s,%s,%s,%s)""", (item['id'], item['sizes'],item['available'],item['light'], item['title'], item['stock']))
			
			
			self.conn.commit()
			print "LOADING ITEM IN PIPELINE!---------------------"
		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
		return item    



#for salming  items
class EhamatchesPipeline(object):

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
        self.cursor.execute("""TRUNCATE TABLE dwxf_eha_matches""")
        self.conn.commit()
        
        

    def process_item(self, item, spider):
		try:
			self.cursor.execute("""INSERT dwxf_eha_matches SET type=%s, home_team=%s, away_team=%s, date=%s, venue=%s,isgd=%s """, (item['itemType'], item['itemHome'], item['itemAway'], item['itemDate'], item['itemVenue'],item['itemIsGD']))
			self.conn.commit()
		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
		return item 
		
		
#for salming  items
class SporteasyPipeline(object):

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
        self.cursor.execute("""TRUNCATE TABLE dwxf_londongd_events_sporteasy""")
        self.conn.commit()
        
        

    def process_item(self, item, spider):
	    print "ITEM--------------"
	    print item
	    try:
	    	self.cursor.execute("""INSERT dwxf_londongd_events_sporteasy SET eventId=%s, date=%s, type=%s, team=%s, location=%s,locationLink=%s,name=%s, attendees=%s, linkevent=%s """, (item['itemEventid'], item['itemDate'], item['itemType'], item['itemTeam'], item['itemLocation'],item['itemLocationLink'],item['itemName'],item['itemAttendees'],item['itemLinkEvent']))
	    	self.conn.commit()
	    except MySQLdb.Error, e:
	    	print "Error %d: %s" % (e.args[0], e.args[1])
		return item 


#for the categories
class KempacatPipeline(object):

    def __init__(self):
        #print "KEMPA CAT PIPELINE---------------------------------------"
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
        	logging.log("Added to MongoDB database!",level=log.DEBUG, spider=spider)
            
        return item          