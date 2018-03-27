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
        	self.collection.update({'itemId':item['itemId']},dict(item), upsert= True)
        	logging.log("Added to MongoDB database!",level=log.DEBUG, spider=spider)
        	print "Added to MongoDB database!"+item['itemId'];
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
            logging.log(logging.ERROR, "Error %d: %s" % (e.args[0], e.args[1]))

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
		except MySQLdb.Error, e:
			logging.log(logging.ERROR, "Error %d: %s" % (e.args[0], e.args[1]))
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
        
        

    def process_item(self, item, spider):
		try:
			#UNIQUEID: TYPE_HOME_AWAY_TIMESTAMP
			itemHomeT = item['itemHome'].replace(" ", "").upper()[:3]
			itemAwayT = item['itemAway'].replace(" ", "").upper()[:3]
			dateT = item['itemDate'].strftime("%s")
			uniqueID = str(item['itemType'])+str(itemHomeT)+str(itemAwayT)+str(dateT)
			

			
			cursor = self.conn.cursor()
			cursor.execute("""
			    INSERT INTO dwxf_eha_matches 
			        (uniqueID, type, home_team, away_team, date, venue, isgd)
			    VALUES 
			        (%s, %s, %s, %s, %s, %s, %s) 
			    ON DUPLICATE KEY UPDATE 
			        type  = VALUES(type),
			        home_team  = VALUES(home_team),
			        away_team  = VALUES(away_team),
			        date  = VALUES(date),
			        venue  = VALUES(venue),
			        isgd   = VALUES(isgd) ;
			               """, (uniqueID, item['itemType'], item['itemHome'], item['itemAway'], item['itemDate'], item['itemVenue'],item['itemIsGD'])
			              )
			self.conn.commit()		
			
			
		except MySQLdb.Error, e:
			logging.log(logging.ERROR, "Error %d: %s" % (e.args[0], e.args[1]))
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
	    try:
	    	self.cursor.execute("""INSERT dwxf_londongd_events_sporteasy SET eventId=%s, date=%s, type=%s, team=%s, location=%s,locationLink=%s,name=%s, attendees=%s, linkevent=%s """, (item['itemEventid'], item['itemDate'], item['itemType'], item['itemTeam'], item['itemLocation'],item['itemLocationLink'],item['itemName'],item['itemAttendees'],item['itemLinkEvent']))
	    	self.conn.commit()
	    except MySQLdb.Error, e:
	    	logging.log(logging.ERROR, "Error %d: %s" % (e.args[0], e.args[1]))
		return item 


#for the categories
class KempacatPipeline(object):

    def __init__(self):

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