# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ApeItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    music = scrapy.Field()
    file_format = scrapy.Field()
    info = scrapy.Field()
    album = scrapy.Field()
    bits = scrapy.Field()
    size = scrapy.Field()
    language = scrapy.Field()
    date = scrapy.Field()
    download_url = scrapy.Field()
    download_password = scrapy.Field()







