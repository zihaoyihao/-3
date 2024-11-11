import scrapy
import json
import re

class StocksSpider(scrapy.Spider):
    name = 'stocks'

    # 股票分类及接口参数
    cmd = {
        "沪深京A股": "f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048",
        "上证A股": "f3&fs=m:1+t:2,m:1+t:23",
        "深证A股": "f3&fs=m:0+t:6,m:0+t:80",
        "北证A股": "f3&fs=m:0+t:81+s:2048",
    }

    start_urls = []

    def start_requests(self):
        for market_code in self.cmd.values():
            for page in range(1, 3):  # 爬取前两页
                url = f"https://98.push2.eastmoney.com/api/qt/clist/get?cb=jQuery&pn={page}&pz=20&po=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&dect=1&wbp2u=|0|0|0|web&fid={market_code}&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152"
                yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # 提取JSON格式数据
        data = response.text
        left_data = re.search(r'^.*?(?=\()', data)

        if left_data:
            left_data = left_data.group()
            data = re.sub(left_data + '\(', '', data)
            data = re.sub('\);', '', data)

            try:
                stock_data = json.loads(data)
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON Decode Error: {e}")
                return  # 返回以避免后续操作

            self.logger.info(f"Parsed JSON Data: {json.dumps(stock_data, indent=4, ensure_ascii=False)}")  # 打印解析后的数据

            if 'data' in stock_data and 'diff' in stock_data['data']:
                for key, stock in stock_data['data']['diff'].items():  # 遍历 diff 字典
                    # 在此添加调试信息，检查每个股票的数据
                    self.logger.debug(f"Stock Data: {stock}")
                    yield {
                        'bStockNo': stock.get("f12", "N/A"),
                        'bStockName': stock.get("f14", "N/A"),
                        'fLatestPrice': stock.get("f2", "N/A"),
                        'fChangeRate': stock.get("f3", "N/A"),
                        'fChangeAmount': stock.get("f4", "N/A"),
                        'fVolume': stock.get("f5", "N/A"),
                        'fTurnover': stock.get("f6", "N/A"),
                        'fAmplitude': stock.get("f7", "N/A"),
                        'fHighest': stock.get("f15", "N/A"),
                        'fLowest': stock.get("f16", "N/A"),
                        'fOpeningPrice': stock.get("f17", "N/A"),
                        'fPreviousClose': stock.get("f18", "N/A")
                    }
            else:
                self.logger.warning("No 'data' or 'diff' found in stock_data.")
        else:
            self.logger.warning("Left data not found in response.")