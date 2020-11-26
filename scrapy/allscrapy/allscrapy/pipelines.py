# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
import pymongo
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class AllscrapyPipeline:
    
    client = pymongo.MongoClient('192.168.1.141:27017')
    
    def process_item(self, item, spider):
        
        db = self.client['mongodb_for_new_things']
        collection = db['new_qq_total']
        
        mongo_data = collection.find({})
        get_mongo_url_list = []
        for data in mongo_data:
            get_mongo_url_list.append(data['url'])
            
            
        mongo_item = dict(item)
        if mongo_item['url'] not in get_mongo_url_list:
            
            collection.insert_one(mongo_item)
            collection.create_index([("time_decline", pymongo.ASCENDING)], expireAfterSeconds=43200)
        # del mongo_item['image_urls']
        # del mongo_item['image_path']
        return item


# class ImagesPipeline(ImagesPipeline):
    
#     def get_media_requests(self, item, info):
        
#         for image_url in item['image_urls']:
#             yield scrapy.Request(image_url, meta={'title':item['title']})
    
#     def file_path(self, request, response=None, info=None, *, item = None):
        
#         dir_name = request.meta['title']
#         image_name = request.url.split('/')[-1]
#         file_name = f'{dir_name}/{image_name}'
#         return file_name
    
#     def item_completed(self, results, item, info):
        
#         image_path = results[0][1].get("path")
#         if not image_path:
#             raise DropItem("image download failed")
#         item["image_path"]= image_path
        
#         return item

