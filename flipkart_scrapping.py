# -*- coding: utf-8 -*-
"""Flipkart_scrapping.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bP4Lpy_CMsO6NBKxM1bUkjpGV2sAv8kt
"""

import os
import re
import requests
import time
import pandas as pd
import pygsheets
import unicodedata
from bs4 import BeautifulSoup as bs
from datetime import datetime
from pytz import timezone

path = 'solid-hope-363110-1c5cd2cd25cf.json'
sheet_id = '16-1AO0iPFTj6FlQpqmT9UmrhHqPrFaXwGVhWtcfzK7w'
URL = "https://www.flipkart.com/google-pixel-6a-charcoal-128-gb/p/itme5ae89135d44e?pid=MOBGFKX5YUXD74Z3&lid=LSTMOBGFKX5YUXD74Z3MXA2OB&marketplace=FLIPKART&q=google+pixel+6a&store=tyy%2F4io&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_2_12_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_12_na_na_na&fm=organic&iid=a3b929d6-28cb-496d-97f8-f56a8096363d.MOBGFKX5YUXD74Z3.SEARCH&ppt=hp&ppn=homepage&ssid=86u2t4xoxc0000001671979563355&qH=02ccfad575fc2cbe"
gc = pygsheets.authorize(service_account_file = path)
gsheet_1 = gc.open_by_key(sheet_id)

def extract_fk_price(url):
    request = requests.get(url)
    soup = bs(request.content,'html.parser')
    product_name = soup.find("span",{"class":"B_NuCI"}).get_text()
    new_str = unicodedata.normalize("NFKD", product_name)
    price = soup.find("div",{"class":"_30jeq3 _16Jk6d"}).get_text()
    prince_int = int(''.join(re.findall(r'\d+', price)))
    time_now = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M')
    return [new_str, prince_int, time_now]

output = extract_fk_price(URL)
df = pd.DataFrame([output], columns = ["Product", "Price", "Date Time"])

df

ws_1 = gsheet_1.worksheet()
sheet_df = ws_1.get_as_df()

if sheet_df.empty:
    ws_1.set_dataframe(df,
                     (1,1))
else:
    df = pd.concat([sheet_df, df], 
                   ignore_index=True)
    ws_1.set_dataframe(df,
                     (1,1))

"""link to [Gsheet](https://docs.google.com/spreadsheets/d/16-1AO0iPFTj6FlQpqmT9UmrhHqPrFaXwGVhWtcfzK7w/edit#gid=0)"""

