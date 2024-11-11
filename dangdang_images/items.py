# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DangdangImagesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
import scrapy

class DangdangImagesItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()