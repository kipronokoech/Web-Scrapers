from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

#Lets define the URL

url="https://archive.org/details/opensource_movies"

# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse HTML code for the entire site
soup = BeautifulSoup(html_content, "lxml")
#print(soup.prettify()) # print the parsed data of html

movies_collection = soup.find("div", attrs={"id": "ikind--downloads"})

# Scrape one movie

aMovie = movies_collection.find_all("div", attrs={"class": "item-ia"})
first = aMovie[17]
#print(first.prettify())
#getting the title of the movie
title = (first.find("div",attrs={"class":"ttl"})).text
title = title.strip()
# Getting the views count of the movie
views = first.find_all("h6",attrs={"class":"stat"})[0].nobr.text
# Stars count
stars = first.find_all("h6",attrs={"class":"stat"})[1].text
# example output of above line if "favorite            12 "
# below line will extract the number from the string above
stars = re.findall("\d+",stars)[0]

comments =  first.find_all("h6",attrs={"class":"stat"})[2].text
comments = re.findall("\d+",comments)[0]

posted_on = ((first.find_all("div",attrs={"class":"hidden-tiles"}))[1]).nobr.text
print(stars)
print(title)
print(views)
print(comments)
print(posted_on)


# We now write one movie details into text file
# JUst like we have comma for CSV we will use # as the separator
# Lets write the titles first
with open("./output/oneMovie.txt","w+") as fp:
    #lets write the titles first
    fp.write("Title#Views#Stars#Comments#Posted_on\n")


# Lets now write details into the
with open("./output/oneMovie.txt","a+") as fp:
    #lets write the details
    one_movie_details = "#".join((title, views, stars, comments, posted_on))
    fp.write(one_movie_details+"\n")

























#https://archive.org/details/opensource_movies
#https://archive.org/details/opensource_movies?&sort=-downloads&page=1

#https://archive.org/details/opensource_movies?&sort=-downloads&page=2
#https://archive.org/details/opensource_movies?&sort=-downloads&page=3
#https://archive.org/details/opensource_movies?&sort=-downloads&page=4