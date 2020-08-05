# import necessary packages
from bs4 import BeautifulSoup
import requests

# URL

url = "https://www.kilimall.co.ke/new/commoditysearch"

# Make a request to fetch raw HTML content

html_content = requests.get(url).text

# Parse the HTML code for the entire site

soup = BeautifulSoup(html_content,"lxml")



one_card = soup.find_all("div",attrs={"class":"el-col-6"})

print(one_card)