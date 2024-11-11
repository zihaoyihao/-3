from setuptools import setup, find_packages

setup(
    name='stocks_scraper',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'scrapy',
        'pymysql',
    ],
    entry_points={
        'scrapy.spiders': [
            'stocks = D:\数据采集作业3\dangdang_images\stock_scraper',
        ],
    },
)