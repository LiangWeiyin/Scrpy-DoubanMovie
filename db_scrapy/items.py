# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DbScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table = 'meta'

    title = scrapy.Field()
    year = scrapy.Field()
    director = scrapy.Field()
    actors = scrapy.Field()
    tags = scrapy.Field()
    rating = scrapy.Field()
    rating_people = scrapy.Field()
    country = scrapy.Field()
    summary = scrapy.Field()
    pic_url = scrapy.Field()
