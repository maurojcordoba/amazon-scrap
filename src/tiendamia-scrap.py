
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from selenium import webdriver
from database import DataBase
import re

def get_url(asin):
    """genera url"""
    template = 'https://tiendamia.com/ar/producto?amz={}'
    
    url = template.format(asin)    

    return url

def get_item(soup,asin):
    #product_name = soup.find('div','product-name')

    # nombre
    #try:
    #    name = product_name.h1.text
    #except AttributeError:
    #    return

    # stock y peso
    description = soup.find('div','short-description')
    try:
        stock = description.find('span', {'id':'stock_producto_ajax'}).text.strip()
    except AttributeError:
        return

    weight = description.find('span', {'id':'weight_producto_ajax'}).text
    weight = weight.replace('.',',')

    # precio
    price_parent = soup.find('div','product-price-box-wrap')
    price = price_parent.find('span', {'id':'allfinalpricecountry_ar_producto_ajax'}).text
    
    
    # imagenes
    # images_parent = soup.find('div','tumbSlider')
    # images = []
    # for image in images_parent.find_all('a',{'id':'mainthumb_link_producto_ajax'}):
    #     images.append(image.get('href'))
    # 
    # images =json.dumps(images)

    result = (price, stock, weight )

    return result

def main():
    # conexion a base
    database = DataBase()

    # iniciar webdriver
    driver  = webdriver.Chrome()

    #cambio codificacion de caracteres
    (driver.page_source).encode('utf-8')

    records = database.amazon_get_items_tm()  

    for record in records:        
        id = record[0]
        asin = record[1]        

        url = get_url(asin)
        driver.get(url)        

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        result = get_item(soup,asin)        
        
        # guardar resultados
        if result:                       
            p = re.search('(\d+\.\d*)', result[0])
            if p:
                price_tm = p.group(1)
            else:
                price_tm = '' 
            
            m = re.search('(\d+,\d*)', result[2])
            if m:
                weight_tm = m.group(1)
            else:
                weight_tm = ''

            stock_tm = result[1]

            database.amazon_update_item(True,price_tm,stock_tm,weight_tm,url,id)
        else:
            database.amazon_update_item(False,'','','','',id)

    database.close()
    driver.close()

main()
