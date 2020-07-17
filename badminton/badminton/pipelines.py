# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
client = pymongo.MongoClient('mongodb+srv://OwOY:{password}@test-g7qjf.mongodb.net/test?retryWrites=true&w=majority')
db = client.test
collection = db.badminton
class BadmintonPipeline:
    def process_item(self, item, spider):
        
        
        info = dict(item)
        result = collection.insert_one(item)


        return item
