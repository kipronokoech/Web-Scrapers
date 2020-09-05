# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector

class AmazonPipeline(object):
    def __init__(self):
        self.establish_connection()
        self.create_table()
    def establish_connection(self):
        self.connection = mysql.connector.connect(
        host = "127.0.0.1",
        port = "3306",
        user = "root",
        password = "destinyx2719*KE",
        database = "amazon",
        auth_plugin='mysql_native_password')
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS amazon_table""")
        self.cursor.execute("""CREATE TABLE amazon_table(
        	product_asin TEXT,
        	product_name TEXT,
        	product_stars TEXT,
        	product_reviews TEXT,
        	product_price TEXT,
        	image_link TEXT)""")

    def process_item(self, item, spider):
        self.store_data(item)
        return item
    def store_data(self,item):
        # self.cursor.execute("""INSERT INTO books_table VALUES(?,?,?)""",\
        # 	(item["titles"],item["prices"],item["availability"]))
        self.cursor.execute("""INSERT INTO amazon_table VALUES(%s,%s,%s,%s,%s, %s)""",\
        	(item["product_asin"],item["product_name"],item["product_stars"],\
        		item["product_reviews"],item["product_price"],item["image_link"]))
        self.connection.commit()
