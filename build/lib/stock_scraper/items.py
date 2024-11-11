# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StockScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
import scrapy

import scrapy

class StocksScraperItem(scrapy.Item):
    bStockNo = scrapy.Field()
    bStockName = scrapy.Field()
    fLatestPrice = scrapy.Field()
    fChangeRate = scrapy.Field()
    fChangeAmount = scrapy.Field()
    fVolume = scrapy.Field()
    fTurnover = scrapy.Field()
    fAmplitude = scrapy.Field()
    fHighest = scrapy.Field()
    fLowest = scrapy.Field()
    fOpeningPrice = scrapy.Field()
    fPreviousClose = scrapy.Field()