from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import re
import time

# path into driver executable
PATH = "/home/kiprono/chromedriver"
# lauch a chrome session
driver = webdriver.Chrome(PATH)

# Define our URL

url = "https://www.kilimall.co.ke/new/"

#get the page source
driver.get(url)
# find the search field so that we will use this to filter items
# using XPath
search_box=driver.find_element_by_xpath("//*[@id='__layout']/section/header/div/div[2]/div[2]/div[1]/div[1]/input")

# just clear in case there are prefilled characters
search_box.clear() 
#search for laptops
search_box.send_keys("Laptops")
#click enter
search_box.send_keys(Keys.RETURN)

#pause execution so that the page finishes loading
#this value changes based on how fast the page loads
time.sleep(10)

# get details of one laptop
page_content = driver.find_elements_by_class_name("el-col-6")
print(len(page_content))
print(page_content[30].find_element_by_class_name("wordwrap").text)
print(page_content[30].find_element_by_class_name("wordwrap-price").text)
quit()
prices = page_content[30].find_element_by_class_name("wordwrap-price")
price_before_discount = prices.find_elements_by_tag_name("span")[1].text
price_after_discount = prices.find_elements_by_tag_name("span")[0].text
discount_text = page_content[30].find_element_by_class_name("greenbox").text
discount = int(re.findall("\d+", discount_text)[0])
print(discount)
rating = page_content[30].find_element_by_class_name("rateList").get_attribute("aria-valuenow")
reviews_text = page_content[30].find_element_by_class_name("sixtwo").text
reviews = int(re.findall("\((.*?)\)",reviews_text)[0])
print(reviews)
dispatchment = page_content[30].find_element_by_class_name("frommall").text
print(dispatchment)



#get the details for all laptops in all pages

# Initialize an empty list to hold all the details we need for all computers
all_details = []
try:
	# loop through all the 4 pages containing the laptops
	for i in range(4):
		#Locate the the "next" page button
		next_page_button = driver.find_element_by_xpath("//*[@id='__layout']/section/main/div/div[2]/section/section/div[3]/div/button[2]/i")
		# locate all items in the page
		page_content = driver.find_elements_by_class_name("el-col-6")
		#loop through all elements in the page
		for j in range(len(page_content)):
			description = page_content[j].find_element_by_class_name("wordwrap").text
			#Capture the prices - both before and after discount
			prices = page_content[j].find_element_by_class_name("wordwrap-price")
			#Price after discount will come first
			price_after_discount = prices.find_elements_by_tag_name("span")[0].text
			try: # We include exceptions handling blocks to captures cases where no discount is given
				# Price before discount comes second
				price_before_discount = prices.find_elements_by_tag_name("span")[1].text
			except:
				# if no dicount is given price before and afrer are all the same
				price_after_discount = price_before_discount
			try:
				#Locate discount text
				discount_text = page_content[j].find_element_by_class_name("greenbox").text
				# Extract the discount value using regex expression
				discount = int(re.findall("\d+", discount_text)[0])
			except:
				discount=None
			# locate current rating and pick the attribute value
			rating = page_content[j].find_element_by_class_name("rateList").get_attribute("aria-valuenow")
			# Locate reviews text
			reviews_text = page_content[j].find_element_by_class_name("sixtwo").text
			# Use regex to pick the value within brackers
			reviews = int(re.findall("\((.*?)\)",reviews_text)[0])
			# Locate dispatchment type: Local or Overseas
			dispatchment = page_content[j].find_element_by_class_name("frommall").text
			# Define a dictionary to hold all the details of interest
			r = {
			"Product Description": description,
			"Price_before_discount": price_before_discount,
			"Price_after_discount": price_after_discount,
			"Discount": discount,
			"Rating":rating,
			"Number of Reviews":reviews,
			"Dispatchment":dispatchment
			}
			# Append the dictonary to the list that is all the details collected thus far
			all_details.append(r)


		#move to the next page by clicking the next button
		next_page_button.click()
		#pauce Python execution until the new page loads completely
		time.sleep(10)
except:
	#close the browser in case we run into any error
	driver.close()


# write the result into CSV file
df = pd.DataFrame(all_details)
# just to rearrange the columns
df = df[list(r.keys())]
df.to_csv("laptops.csv",index=False)

#close all the browser tabs
driver.quit()
