from csv import reader
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from selenium import webdriver
import json
from database import DataBase


def get_url(asin):
    """genera url"""
    #template = 'https://www.buscalibre.com.ar/amazon?url=https%3A%2F%2Fwww.amazon.com%2Fdp%2F{}&t=tetraemosv4'
    template = 'https://www.buscalibre.com.ar/boton-prueba-gp?t=tetraemosv4&envio-avion=1&codigo={}-com&sitio=amazon&version=2&condition=new'
    url = template.format(asin)    

    return url

def get_item(soup,url,price_amz,img,asin):
    product_name = soup.find('div','product-name')

    # nombre
    try:
        name = product_name.h1.text
    except AttributeError:
        return

    # stock y peso
    description = soup.find('div','short-description')
    stock = description.find('span', {'id':'stock_producto_ajax'}).text.strip()
    weight = description.find('span', {'id':'weight_producto_ajax'}).text
    weight = weight.replace('.',',')

    # precio
    price_parent = soup.find('div','product-price-box-wrap')
    price = price_parent.find('span', {'id':'allfinalpricecountry_ar_producto_ajax'}).text
    
    
    # imagenes
    images_parent = soup.find('div','tumbSlider')
    images = []
    for image in images_parent.find_all('a',{'id':'mainthumb_link_producto_ajax'}):
        images.append(image.get('href'))
    
    images =json.dumps(images)

    result = (name, asin, price_amz, img, stock, weight, url,price, images)

    return result

def main():    
    # conexion a base
    database = DataBase()

    records = database.amazon_get_items()    
    if(len(records) != 0):

        # iniciar webdriver
        driver  = webdriver.Chrome()
        
        #cambio codificacion de caracteres
        (driver.page_source).encode('utf-8')
    
    
        for record in records:        
            id = record[0]
            asin = record[1]

            url = get_url(asin)
            
            driver.get(url)        

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            price_parent = soup.find('div','precio-transporte')
            if price_parent:
                price_bl = price_parent.find('span', 'price').text
                database.amazon_update_item(True,price_bl,id)
            else:
                database.amazon_update_item(False,'',id)
        
        database.close()
        driver.close() 
    else:
        print("NO SE ENCONTRARON PRODUCTOS PARA VERIFICAR")


main()
