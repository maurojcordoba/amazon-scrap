from csv import reader
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from selenium import webdriver
import pymysql
import json
from database import DataBase
import time
import random

def get_url(page):
    """genera url"""
    #template = 'https://www.buscalibre.com.ar/amazon?url=https%3A%2F%2Fwww.amazon.com%2Fdp%2F{}&t=tetraemosv4'
    template = 'https://www.walmart.com/browse/games-puzzles/games-by-age/4171_4191_2335373?page={}&affinityOverride=default'
    url = template.format(page)    

    return url

def get_item(tag):
    description=asin=price=img=url=''

    asin = tag['data-item-id']
    # product_name = soup.find('div','product-name')

    # # nombre
    # try:
    #     description = product_name.h1.text
    # except AttributeError:
    #     return

    # # stock y peso
    # description = soup.find('div','short-description')
    # stock = description.find('span', {'id':'stock_producto_ajax'}).text.strip()
    # weight = description.find('span', {'id':'weight_producto_ajax'}).text
    # weight = weight.replace('.',',')

    # # precio
    # price_parent = soup.find('div','product-price-box-wrap')
    # price = price_parent.find('span', {'id':'allfinalpricecountry_ar_producto_ajax'}).text
    
    
    # # imagenes
    # images_parent = soup.find('div','tumbSlider')
    # images = []
    # for image in images_parent.find_all('a',{'id':'mainthumb_link_producto_ajax'}):
    #     images.append(image.get('href'))
    
    # images =json.dumps(images)

    item = (description, asin, price, img, url)

    return item

#def main():
# conexion a base
database = DataBase()

# iniciar webdriver
driver  = webdriver.Chrome()

#cambio codificacion de caracteres
(driver.page_source).encode('utf-8')


for page in range(1,3):
    print('Page: ', page)
    url = get_url(page)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tags = soup.find_all('div','mid-gray')
    
    for tag in tags:
        
        item = get_item(tag)
        print(item)
        # if record:        
        #     database.amazon_tmp_add(record)
        # else:
        #     print('Not extract record: ',item)
    time.sleep(random.uniform(2.0,3.0))
database.close()
#    driver.close()

#main()
