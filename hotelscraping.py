import requests
from bs4 import BeautifulSoup
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Use this guide to select your web browser of choice

Chrome_service = ChromeService(ChromeDriverManager().install())

driver = webdriver.Chrome(service=Chrome_service)
driver.implicitly_wait(5)

URL = "https://zh.hotels.com/Hotel-Search?adults=2&d1=2023-09-29&d2=2023-09-30&destination=London%2C%20England%2C%20United%20Kingdom&endDate=2023-12-06&latLong=51.50746%2C-0.127673&locale=en_HK&pos=HCOM_HK&regionId=2114&rooms=1&semdtl=&siteid=300000039&sort=RECOMMENDED&startDate=2023-12-05&theme=&useRewards=false&userIntent="


driver.get(URL)
time.sleep(10)

response=requests.get(URL)

subhtml = driver.page_source
soup= BeautifulSoup(subhtml, 'html.parser')

prices = soup.find_all('div', class_="uitk-text uitk-type-500 uitk-type-medium uitk-text-emphasis-theme")
prices_l = []
for price in prices:
    prices_l.append(price.text)
prices_l = [float(price.replace('HK$','').replace(',','')) for price in prices_l]

hotels = soup.find_all('h3', class_="uitk-heading uitk-heading-5 overflow-wrap uitk-layout-grid-item uitk-layout-grid-item-has-row-start")
hotels_l = []
for hotel in hotels:
    hotels_l.append(hotel.text)
    
reviews = soup.find_all('div', class_="uitk-text truncate-lines-2 uitk-type-200 uitk-type-regular uitk-text-default-theme")
reviews_l = []
for review in reviews:
    reviews_l.append(review.find('span', class_='is-visually-hidden').text)

reviews_l = [int(review.replace(',', '').split()[0]) for review in reviews_l]

ratings = soup.find_all('span', class_="uitk-badge-base-text")
ratings_l = []
for rating in ratings:
    try:
        ratings_l.append(float(rating.text))
    except ValueError:
        ratings_l.append(float(0))
    
comments = soup.find_all('div', class_="uitk-text truncate-lines-2 uitk-type-300 uitk-type-medium uitk-text-emphasis-theme")
comments_l = []
for comment in comments:
    comments_l.append(comment.find('span', class_='is-visually-hidden').text)
    
table_data = {
    'Hotel': hotels_l,
    'Price': prices_l

}

hotel_df = pd.DataFrame(table_data)
print(hotel_df)

sns.set_style('whitegrid')



plt.figure(figsize=(6,4))
sns.kdeplot(hotel_df['Price'], fill=True)
plt.title('Distribution of Price')
plt.xlabel('Price')
plt.ylabel('Density')
plt.show()