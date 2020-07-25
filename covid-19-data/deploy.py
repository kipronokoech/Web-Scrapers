# in this script we will deploy the output of the other
# py files into excel file
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from scraper2 import Scraper
import numpy as np

#To understand the basics go to: https://gspread.readthedocs.io/en/latest/

# Defining the scope of file interaction
scope = (["https://spreadsheets.google.com/feeds",
          "https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive.file",
          "https://www.googleapis.com/auth/drive"])
#loading the credentials file
creds =  ServiceAccountCredentials.from_json_keyfile_name("./assets/api.json",scope)
client = gspread.authorize(creds)
#open google sheet file named "data", the worksheet
#named "test_world"
#to make a new sheet in data file uncomment the following two lines
#sheet = client.open("data")
#sheet.add_worksheet(title="test_world", rows="100", cols="20")
sheet = client.open("data").worksheet("test_world")
#above line is same us the following two:
# sheet = client.open("data")
#sheet = sheet.worksheet("test_world")
#get all the record on the sheet
data = sheet.get_all_records()
#getting the row
row = sheet.row_values(3)
print(row)
#getting the column
col = sheet.col_values(1)
print(col)
#get values on a specific cell
cell = sheet.cell(1,2).value
print(cell)
#insert row
#sheet.resize(len(data))
insert_row = ["Yae",47600]
#sheet.insert_row(insert_row,1)
#sheet.delete_row(1)
#sheet.insert_row(insert_row,1)
data2 = sheet.get_all_records()
print(len(data2))
sheet.insert_row(["after the last"],len(data2)+2)
sheet.delete_rows(len(data2)+1)
data2 = sheet.get_all_records()
sheet.insert_row(["last"],len(data2)+1)

#We can now go ahead and deploy our data
#lets scrap the and store it into a varibale df
sheet = client.open("data").worksheet("World")
df = Scraper("https://www.worldometers.info/coronavirus/")
#gspread cant deploy values with NaN so we need to fix that
df = df.replace(np.nan, '', regex=True)

sheet.update([df.columns.values.tolist()] + df.values.tolist())

#DONE -  Now you can go check your worksheet

