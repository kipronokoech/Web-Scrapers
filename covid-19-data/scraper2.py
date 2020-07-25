# importing the libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd

def Scraper(url):
    # Lets define the URL

    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text

    # Parse HTML code for the entire site
    soup = BeautifulSoup(html_content, "lxml")
    # print(soup.prettify()) # print the parsed data of html

    # the head will form our columns
    # we pick the id of the table we want to scrape and extract HTML code for that particular table only
    covid_table = soup.find("table", attrs={"id": "main_table_countries_today"})
    head = covid_table.thead.find_all("tr")
    # the headers are contained in this HTML code
    headings = []
    for th in head[0].find_all("th"):
        # remove any newlines and extra spaces from left and right
        # headings.append(td.b.text.replace('\n', ' ').strip())
        headings.append(th.text.replace("\n", "").strip())
    body = covid_table.tbody.find_all("tr")
    # here is one example of HTML snippet for one row
    # lets declare empty list data that will hold all rows data
    data = []
    for r in range(1, len(body)):
        row = []  # empty lsit to hold one row data
        for tr in body[r].find_all("td"):
            row.append(tr.text.replace("\n", "").strip())
            # append row data to row after removing newlines escape and triming unnecesary spaces
        data.append(row)

    # data contains all the rows excluding header
    # row contains data for one row
    # We can now pass data into a pandas dataframe
    # with headings as the columns
    df = pd.DataFrame(data, columns=headings)
    data = df[df["#"] != ""].reset_index(drop=True)
    # Data points with # value are the countries of the world while the data points with
    # null values for # columns are features like continents totals etc
    data = data.drop_duplicates(subset=["Country,Other"])
    # Reason to drop duplicates : Worldometer reports data for 3 days: today and 2 days back
    # I found out that removing duplicates removes the values for the bast two days and keep today's
    # We can drop the following columns - Opinion
    cols = ['#',
            'Tot\xa0Cases/1M pop',
            'Deaths/1M pop',
            'Tests/1M pop',
            'Population',
            '1 Caseevery X ppl',
            '1 Deathevery X ppl',
            '1 Testevery X ppl']
    data_final = data.drop(cols, axis=1)

    return data_final
