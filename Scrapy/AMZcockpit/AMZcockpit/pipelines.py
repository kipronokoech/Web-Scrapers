# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector


class AmzcockpitPipeline(object):
    def __init__(self):
        self.establish_conn()
        self.create_table()
    def establish_conn(self):
        self.conn = mysql.connector.connect(
        host = "127.0.0.1",
        port = "3306",
        user = "root",
        password = "destinyx2719*KE",
        database = "amazon_cockpit",
        auth_plugin='mysql_native_password')
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("""DROP TABLE IF EXISTS keywords_table""")
        self.cur.execute("""CREATE TABLE keywords_table(
        keyword TEXT,
        product_asin TEXT,
        overall_rank TEXT,
        inpage_rank TEXT,
        page_number TEXT,
        sponsored TEXT)""")
    def process_item(self, item, spider):
        self.store_data(item)
        return item
    def store_data(self,item):
        # self.cur.execute("""INSERT INTO books_table VALUES(?,?,?)""",\
        # 	(item["titles"],item["prices"],item["availability"]))
        self.cur.execute("""INSERT INTO keywords_table VALUES(%s,%s,%s,%s,%s, %s)""",\
        	(item["keyword"],item["product_asin"],str(item["overall_rank"]),\
        		item["inpage_rank"],item["page_number"],item["sponsored"]))
        self.conn.commit()
        self.conn.close()



AmzcockpitPipeline()
