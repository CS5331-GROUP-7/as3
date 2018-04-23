# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
    url = scrapy.Field()
    type = scrapy.Field()
    param = scrapy.Field()
    headers = scrapy.Field()
    cookies = scrapy.Field()

# class CookieItem(scrapy.Item):
    # url = scrapy.Field()
    # cookies = scrapy.Field()
