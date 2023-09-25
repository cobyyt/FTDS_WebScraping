import requests
from bs4 import BeautifulSoup
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


url = 'https://www.hotels.com/Hotel-Search?adults=2&d1=2023-09-29&d2=2023-09-30&destination=London%2C%20England%2C%20United%20Kingdom&endDate=2023-09-30&latLong=51.50746%2C-0.127673&regionId=2114&rooms=1&semdtl=&sort=RECOMMENDED&startDate=2023-09-29&theme=&useRewards=false&userIntent='
response=requests.get(url)

soup= BeautifulSoup(response.content, 'html.parser')

prices = soup.find_all('div', class_="uitk-text uitk-type-500 uitk-type-medium uitk-text-emphasis-theme")
prices_l = []
for price in prices:
    prices_l.append(price.text)
prices_l = [float(price.replace('$','')) for price in prices_l]

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
    ratings_l.append(float(rating.text))
    
comments = soup.find_all('div', class_="uitk-text truncate-lines-2 uitk-type-300 uitk-type-medium uitk-text-emphasis-theme")
comments_l = []
for comment in comments:
    comments_l.append(comment.find('span', class_='is-visually-hidden').text)
    
table_data = {
    'Hotel': hotels_l,
    'Price': prices_l,
    'Comment': comments_l,
    'Rating': ratings_l,
    'Review': reviews_l
}

hotel_df = pd.DataFrame(table_data)
print(hotel_df)

sns.set_style('whitegrid')

plt.figure(figsize=(6,5))
sns.barplot(x='Comment', y='Price', data=hotel_df)
plt.title('Price by Comment')
plt.xlabel('Comment')
plt.ylabel('Price')
plt.show()

plt.figure(figsize=(6,4))
sns.kdeplot(hotel_df['Price'], fill=True)
plt.title('Distribution of Price')
plt.xlabel('Price')
plt.ylabel('Density')
plt.show()