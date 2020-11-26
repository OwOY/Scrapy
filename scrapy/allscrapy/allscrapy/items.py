# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AllscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    content = scrapy.Field()
    time_decline = scrapy.Field()
    
    # images = scrapy.Field()
    # image_urls = scrapy.Field()
    # image_path = scrapy.Field()
    