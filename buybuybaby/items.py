# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags


class BuybuybabyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    ratings = scrapy.Field()
    reviews = scrapy.Field()
    producturl = scrapy.Field()
    
class BabiesrusItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    ratings = scrapy.Field()
    producturl = scrapy.Field()
    pageurl = scrapy.Field()

