# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BocExchangePipeline:
    def process_item(self, item, spider):
        return item
import pymysql
from scrapy.exceptions import DropItem

class BankPipeline:
    def __init__(self, mysql_host, mysql_user, mysql_password, mysql_db, mysql_port):
        self.mysql_host = mysql_host
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_db = mysql_db
        self.mysql_port = mysql_port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST', 'localhost'),
            mysql_user=crawler.settings.get('MYSQL_USER', 'root'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD', ''),
            mysql_db=crawler.settings.get('MYSQL_DB', 'boc_exchange'),
            mysql_port=crawler.settings.get('MYSQL_PORT', 3306),
        )

    def open_spider(self, spider):
        self.connection = pymysql.connect(
            host=self.mysql_host,
            user=self.mysql_user,
            password=self.mysql_password,
            database=self.mysql_db,
            port=self.mysql_port,
            charset='utf8mb4',
            use_unicode=True
        )
        self.cursor = self.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS exchange_rates (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Currency VARCHAR(100),
            TBP DECIMAL(10,2),
            CBP DECIMAL(10,2),
            TSP DECIMAL(10,2),
            CSP DECIMAL(10,2),
            Time VARCHAR(20)
        )
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def process_item(self, item, spider):
        insert_query = """
        INSERT INTO exchange_rates (Currency, TBP, CBP, TSP, CSP, Time)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_query, (
            item['Currency'],
            item['TBP'],
            item['CBP'],
            item['TSP'],
            item['CSP'],
            item['Time']
        ))
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()