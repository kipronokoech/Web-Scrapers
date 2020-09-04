import sqlite3

connection = sqlite3.connect("books.db")
cursor = connection.cursor()

# cursor.execute("""CREATE TABLE books_table(
# 	title TEXT,
# 	price TEXT,
# 	availability TEXT)""")

cursor.execute("""INSERT INTO books_table VALUES('Atomic Abits','20USD','In Stock')""")

connection.commit()
connection.close()