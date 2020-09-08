# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# scrape -> item containers -> JSON/CSV/XML
# scrape ->item containers -> Pipeline -> DB
# import sqlite3
import mysql.connector

class BooksStorePipeline(object):

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
			database = "books_store",
			auth_plugin='mysql_native_password')
		self.cursor = self.connection.cursor()

	def create_table(self):
		self.cursor.execute("""DROP TABLE IF EXISTS books_table""")
		self.cursor.execute("""CREATE TABLE books_table(
			title TEXT,
			price TEXT,
			availability TEXT)""")

	def process_item(self, item, spider):
		print("From Pipeline:",item["titles"])
		self.store_data(item)
		return item
	def store_data(self,item):
		# self.cursor.execute("""INSERT INTO books_table VALUES(?,?,?)""",\
		# 	(item["titles"],item["prices"],item["availability"]))
		self.cursor.execute("""INSERT INTO books_table VALUES(%s,%s,%s)""",\
			(item["titles"],item["prices"],item["availability"]))
		self.connection.commit()
