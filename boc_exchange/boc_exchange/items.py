# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BocExchangeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
import scrapy

class BankItem(scrapy.Item):
    Currency = scrapy.Field()
    TBP = scrapy.Field()      # 现汇买入价
    CBP = scrapy.Field()      # 现钞买入价
    TSP = scrapy.Field()      # 现汇卖出价
    CSP = scrapy.Field()      # 现钞卖出价
    Time = scrapy.Field()     # 时间