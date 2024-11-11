import argparse
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from stock_scraper.spiders import stock_spider  # 替换为您的爬虫模块路径


def main():
    # 设置日志记录
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler("scrapy.log"),
            logging.StreamHandler()
        ]
    )

    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Run the Scrapy spider.')
    parser.add_argument('--spider', type=str, default='stocks', help='Name of the spider to run')
    args = parser.parse_args()

    # 获取Scrapy的设置
    settings = get_project_settings()

    # 创建一个CrawlerProcess实例
    process = CrawlerProcess(settings)

    # 启动爬虫
    process.crawl(stock_spider.StocksSpider)  # 替换为您的爬虫类名

    # 开始爬取
    process.start()


if __name__ == '__main__':
    main()