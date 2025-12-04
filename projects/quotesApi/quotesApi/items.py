# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuotesapiItem(scrapy.Item):
    author     = scrapy.Field()
    authorLink = scrapy.Field()
    tags       = scrapy.Field()
    citation   = scrapy.Field()