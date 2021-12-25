
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import numpy as np
import re


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

# Scrape one category # Travel

#Set up the path to the chrome driver
PATH = "/home/kiprono/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("http://books.toscrape.com/catalogue/category/books_1/page-1.html")

# Lets find all books in the page
incategory = driver.find_elements_by_class_name("product_pod")
#Generate a list of links for each and every book
links = []
for i in range(len(incategory)):
	item = incategory[i]
	#get the href property
	a = item.find_element_by_tag_name("h3").find_element_by_tag_name("a").get_property("href")
	#Append the link to list links
	links.append(a)



all_details = []
# Lets loop through each link to acces the page of each book
for link in links:
	# get one book url
	driver.get(url=link)
	# title of the book
	title = driver.find_element_by_xpath("//*[@id='content_inner']/article/div[1]/div[2]/h1")
	# price of the book
	price = driver.find_element_by_xpath("//*[@id='content_inner']/article/div[1]/div[2]/p[1]")
	# stock - number of copies available for the book
	stock = driver.find_element_by_xpath("//*[@id='content_inner']/article/div[1]/div[2]/p[2]")
	# Stock comes as string
	stock = int(re.findall("\d+",stock.text)[0])
	# Stars - Actual stars are in the tag attribute
	stars = driver.find_element_by_xpath("//*[@id='content_inner']/article/div[1]/div[2]/p[3]").get_attribute("class")
	# convert string to number. Stars are like One, Two, Three ... We need 1,2,3,...
	stars = StarConversion(stars.split()[1])
	# Description
	try:
		description = driver.find_element_by_xpath("//*[@id='content_inner']/article/p")
		description = description.text
	except:
		description = None
	# UPC ID
	upc = driver.find_element_by_xpath("//*[@id='content_inner']/article/table/tbody/tr[1]/td")
	# Tax imposed in the book
	tax = driver.find_element_by_xpath("//*[@id='content_inner']/article/table/tbody/tr[5]/td")
	# Category of the book
	category_a =  driver.find_element_by_xpath("//*[@id='default']/div/div/ul/li[3]/a")

	# Define a dictionary with details we need
	r = {
		"1Title":title.text,
		"2Category":category_a.text,
		"3Stock": stock,
		"4Stars": stars,
		"5Price":price.text,
		"6Tax":tax.text,
		"7UPC":upc.text,
		"8Description": description
	}
	# append r to all details
	all_details.append(r)


time.sleep(4)

driver.close()