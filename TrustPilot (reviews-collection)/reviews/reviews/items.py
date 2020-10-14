# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ReviewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    stars = scrapy.Field()
    review_title = scrapy.Field()
    review_body = scrapy.Field()
    platform = scrapy.Field()
    review_date = scrapy.Field()
    reply_message = scrapy.Field()
