# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmzcockpitItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    keyword = scrapy.Field()
    product_asin = scrapy.Field()
    overall_rank = scrapy.Field()
    inpage_rank = scrapy.Field()
    page_number = scrapy.Field()
    sponsored  = scrapy.Field()