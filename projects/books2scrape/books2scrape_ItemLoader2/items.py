# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy
from   itemloaders.processors import TakeFirst, MapCompose, Join
from   w3lib.html             import remove_tags


def cleanprice(priceval):
    return priceval.replace("£", "").strip()

def uppercode(code):
    return code.upper()

class Books2ScrapeItem(scrapy.Item):
    title        = scrapy.Field(MapCompose(str.strip, remove_tags), output_processor = TakeFirst()) # Retire l'html et les espaces inutiles et prend la prelère valeur
    price        = scrapy.Field(MapCompose(cleanprice), output_processor = TakeFirst())
    product_id   = scrapy.Field(MapCompose(uppercode), output_processor = TakeFirst())
    product_type = scrapy.Field(MapCompose(str.strip), output_processor = TakeFirst())
    stock        = scrapy.Field(MapCompose(str.strip), output_processor = TakeFirst())