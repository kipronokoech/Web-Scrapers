from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import numpy as np
import re


#Set up the path to the chrome driver
PATH = "/home/kiprono/chromedriver"
driver = webdriver.Chrome(PATH)
#parse the page source using get() function
driver.get("http://books.toscrape.com/catalogue/category/books_1/page-1.html")

#We find all the books in the page and just use 1
incategory = driver.find_elements_by_class_name("product_pod")[0]
#local the URL to open the contents of the book
a = incategory.find_element_by_tag_name("h3").find_element_by_tag_name("a").get_property("href")
driver.get(a)
#locate our elements of interest on the page containing book details.
title = driver.find_element_by_xpath("//*[@id='content_inner']/article/div[1]/div[2]/h1")
price = driver.find_element_by_xpath("//*[@id='content_inner']/article/div[1]/div[2]/p[1]")
stock = driver.find_element_by_xpath("//*[@id='content_inner']/article/div[1]/div[2]/p[2]")
stars = driver.find_element_by_xpath("//*[@id='content_inner']/article/div[1]/div[2]/p[3]").get_attribute("class")
stock = int(re.findall("\d+",stock.text)[0])

# This is a fuction to convert stars from string expressions to int
def StarConversion(value):
	if value == "One":
		return 1
	elif value == "Two":
		return 2
	elif value == "Three":
		return 3
	elif value == "Four":
		return 4
	elif value == "Five":
		return 5 

stars = StarConversion(stars.split()[1])

description = driver.find_element_by_xpath("//*[@id='content_inner']/article/p")

upc = driver.find_element_by_xpath("//*[@id='content_inner']/article/table/tbody/tr[1]/td")

tax = driver.find_element_by_xpath("//*[@id='content_inner']/article/table/tbody/tr[5]/td")

category_a =  driver.find_element_by_xpath("//*[@id='default']/div/div/ul/li[3]/a")


r = {
	"Title":title.text,
	"Stock": stock,
	"Stars": stars,
	"Price":price.text,
	"Tax":tax.text,
	"UPC":upc.text,
	"Description": description.text
}

# print all contents of the dictionary
print(r)

time.sleep(3)
driver.quit()

