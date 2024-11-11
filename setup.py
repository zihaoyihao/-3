from setuptools import setup, find_packages

setup(
    name='stock_scraper',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'scrapy',
        'pymysql',
    ],
    entry_points={
        'scrapy.spiders': [
            'stocks = stock_scraper.spiders.stocks:StocksSpider',
        ],
    },
)