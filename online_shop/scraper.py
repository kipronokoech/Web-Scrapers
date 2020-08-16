# import necessary packages
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
# URL

url = "https://www.jumia.co.ke/computing/"

# Make a request to fetch raw HTML content

html_content = requests.get(url).text

# Parse the HTML code for the entire site

soup = BeautifulSoup(html_content,"lxml")


#one card

aPage = soup.find_all("article",attrs={"class":"prd"})

one_card = aPage[0]

one_card = one_card.find("div",attrs={"class":"info"})


product_name = one_card.h3.text
# or product_name2 = one_card.find("h3").text
print(product_name)

current_price = one_card.find("div",attrs={"class","prc"}).text
print(current_price)

old_price = one_card.find("div",attrs={"class","old"}).text
print(old_price)

discount = one_card.find("div",attrs={"class","_dsct"}).text
print(discount)

stars = one_card.find("div",attrs={"class":"stars"}).text
stars = stars.split()[0]
print(stars)


reviews = one_card.find("div",attrs={"class":"rev"}).text
reviews = re.findall("\((.*?)\)",reviews)[0]
print(reviews)



# All 48 cards on one page

cards = []
for index in range(len(aPage)):
	one_card = aPage[index]
	one_card = one_card.find("div",attrs={"class":"info"})
	product_name = one_card.h3.text.lstrip("")
	print(product_name)
	current_price = one_card.find("div",attrs={"class","prc"}).text
	try:
		old_price = one_card.find("div",attrs={"class","old"}).text
	except:
		#if no old price is given pass a NoneType
		old_price = None
	try:
		discount = one_card.find("div",attrs={"class","_dsct"}).text
	except:
		# If no discount is applied pass a NoneType
		discount = None
	try:

		stars = one_card.find("div",attrs={"class":"stars"}).text
		stars = stars.split()[0]

		reviews = one_card.find("div",attrs={"class":"rev"}).text
		reviews = re.findall("\((.*?)\)",reviews)[0]

	except:
		# If no reviews have been given give stars and reviews NoneType
		stars = None
		reviews = None

	card_details = [product_name,old_price,discount,current_price,stars,reviews]
	cards.append(card_details)


df = pd.DataFrame(data=cards,columns=["Product Description","Price(Before Discount)",\
	"Discount","Price(After Discount)","Stars","Number of Reviews"])
print(df)
#df.to_csv("test.csv")


