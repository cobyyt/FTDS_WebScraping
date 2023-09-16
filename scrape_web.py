import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Use this guide the select your web browser of choice


Edge_service = EdgeService(EdgeChromiumDriverManager().install())

driver = webdriver.Edge(service=Edge_service)
driver.implicitly_wait(5)

URL = "https://zh.hotels.com/Hotel-Search?adults=2&d1=2023-09-29&d2=2023-09-30&destination=London%2C+England%2C+United+Kingdom&endDate=2023-09-30&latLong=51.50746%2C-0.127673&locale=en_HK&pos=HCOM_HK&regionId=2114&rooms=1&semdtl=&siteid=300000039&sort=RECOMMENDED&startDate=2023-09-29&theme=&useRewards=false&userIntent="


driver.get(URL)
time.sleep(10)

breads = driver.find_elements(By.TAG_NAME, "a")


print(driver)

