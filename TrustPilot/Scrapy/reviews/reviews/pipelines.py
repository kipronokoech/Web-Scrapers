import json
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter
import mysql.connector
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

class ReviewsPipeline:
	def __init__(self):
		self.establish_connection()
		self.create_table()

	def establish_connection(self):
		# self.connection = sqlite3.connect("books.db")
		self.connection = mysql.connector.connect(
			host = "127.0.0.1",
			port = "3306",
			user = "root",
			password = "destinyx2719*KE",
			database = "reviews",
			auth_plugin='mysql_native_password')
		self.cursor = self.connection.cursor()

	def create_table(self):
		self.cursor.execute("""DROP TABLE IF EXISTS trustpilot_reviews_table""")
		self.cursor.execute(
			"""
			CREATE TABLE trustpilot_reviews_table
				(
					stars TEXT,
				    review_title TEXT,
				    review_body TEXT,
				    platform TEXT,
				    review_date TEXT,
				   	ID TEXT,
				    CompanyReply TEXT,
				    CompanyReplyDate TEXT,
				    CompanyReplyTime TEXT,
				    SNo TEXT
			    )
		    """
		    )

	def process_item(self, item, spider):
		self.store_data(item)
		return item
	def store_data(self,item):
		# self.cursor.execute("""INSERT INTO trustpilot_reviews_table VALUES(?,?,?)""",\
		# 	(item["titles"],item["prices"],item["availability"]))
		self.cursor.execute("""INSERT INTO trustpilot_reviews_table VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",\
			(item["SNo"],item["stars"],item["review_title"],item["review_body"],item["platform"]
				,item["review_date"],item["ID"],item["CompanyReply"]
				,item["CompanyReplyDate"],item["CompanyReplyTime"]))
		self.connection.commit()

# class JsonWriterPipeline(object):
#     def open_spider(self, spider):
#         self.file = open('reviews.json', 'w')
#         # Your scraped items will be saved in the file 'scraped_items.json'.
#         # You can change the filename to whatever you want.
#         self.file.write("[")

#     def close_spider(self, spider):
#         self.file.write("]")
#         self.file.close()

#     def process_item(self, item, spider):
#         line = json.dumps(
#             dict(item),
#             indent = 4,
#             sort_keys = True,
#             separators = (',', ': ')
#         ) + ",\n"
#         self.file.write(line)
#         return item

