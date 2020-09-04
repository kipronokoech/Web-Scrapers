# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
# Extract data -> Temporary containers (items) -> DB

import scrapy


class BooksStoreItem(scrapy.Item):
    # define the fields for your item here like:
    titles = scrapy.Field()
    prices = scrapy.Field()
    availability = scrapy.Field()
