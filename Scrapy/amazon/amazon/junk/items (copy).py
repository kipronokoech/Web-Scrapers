# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class AmazonItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     product_name = scrapy.Field()
#     product_asin = scrapy.Field()
#     product_stars = scrapy.Field()
#     product_reviews = scrapy.Field()
#     product_price = scrapy.Field()
#     image_link = scrapy.Field()

class KeywordItem(scrapy.Item):
	product_asin =  scrapy.Field()