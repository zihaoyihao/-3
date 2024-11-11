# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class StockScraperPipeline:
    def process_item(self, item, spider):
        return item
import pymysql
from scrapy.exceptions import DropItem

class StockPipeline:
    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            port=crawler.settings.get('MYSQL_PORT'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            db=crawler.settings.get('MYSQL_DB'),
        )

    def open_spider(self, spider):
        self.connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()

        import pymysql
        from itemadapter import ItemAdapter

        class StocksScraperPipeline:
            def open_spider(self, spider):
                self.connection = pymysql.connect(
                    host='127.0.0.1',
                    port=33068,
                    user='root',  # 替换为你的MySQL用户名
                    password='160127ss',  # 替换为你的MySQL密码
                    database='spydercourse',  # 数据库名
                    charset='utf8mb4',
                    use_unicode=True,
                )
                self.cursor = self.connection.cursor()

                # 创建表格
                create_table_sql = """
                CREATE TABLE IF NOT EXISTS stocks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    bStockNo VARCHAR(10),
                    bStockName VARCHAR(50),
                    fLatestPrice DECIMAL(10, 2),
                    fChangeRate DECIMAL(5, 2),
                    fChangeAmount DECIMAL(10, 2),
                    fVolume BIGINT,
                    fTurnover DECIMAL(10, 2),
                    fAmplitude DECIMAL(5, 2),
                    fHighest DECIMAL(10, 2),
                    fLowest DECIMAL(10, 2),
                    fOpeningPrice DECIMAL(10, 2),
                    fPreviousClose DECIMAL(10, 2)
                );
                """
                self.cursor.execute(create_table_sql)

            def close_spider(self, spider):
                self.connection.close()

            def process_item(self, item, spider):
                print(f"Storing item: {item}")  # 打印每个存储的项
                try:
                    insert_sql = """
                    INSERT INTO stocks (bStockNo, bStockName, fLatestPrice, fChangeRate, fChangeAmount, fVolume, fTurnover, fAmplitude, fHighest, fLowest, fOpeningPrice, fPreviousClose) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    self.cursor.execute(insert_sql, (
                        item['bStockNo'],
                        item['bStockName'],
                        float(item['fLatestPrice']),
                        float(item['fChangeRate']),
                        float(item['fChangeAmount']),
                        int(item['fVolume']),
                        float(item['fTurnover']),
                        float(item['fAmplitude']),
                        float(item['fHighest']),
                        float(item['fLowest']),
                        float(item['fOpeningPrice']),
                        float(item['fPreviousClose']),
                    ))
                    self.connection.commit()
                except Exception as e:
                    print(f"Error storing item: {e}")
                    print(f"SQL: {insert_sql} | Values: {item}")
                return item