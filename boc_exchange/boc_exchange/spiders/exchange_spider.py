import scrapy
from boc_exchange.items import BankItem

class ExchangeSpider(scrapy.Spider):
    name = "exchange"
    allowed_domains = ["boc.cn"]
    start_urls = ["https://www.boc.cn/sourcedb/whpj/"]

    def parse(self, response):
        # 解析表格数据
        table = response.xpath('//table[@class="table-data"]')[0]
        rows = table.xpath('.//tr')

        for row in rows[1:]:  # 跳过表头
            item = BankItem()
            item['Currency'] = row.xpath('.//td[1]/text()').get().strip()
            item['TBP'] = row.xpath('.//td[2]/text()').get().strip()
            item['CBP'] = row.xpath('.//td[3]/text()').get().strip()
            item['TSP'] = row.xpath('.//td[4]/text()').get().strip()
            item['CSP'] = row.xpath('.//td[5]/text()').get().strip()
            item['Time'] = row.xpath('.//td[6]/text()').get().strip()  # 根据实际情况调整

            yield item