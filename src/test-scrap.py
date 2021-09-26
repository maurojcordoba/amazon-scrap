
from csv import reader
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from selenium import webdriver
import pymysql
import json

class DataBase:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='insertcoin',
            db='scrap'
        )
    
        self.cursor = self.connection.cursor()

   
    def insert_item(self, item):
        name = self.connection.escape_string(item[0])
        sql = "INSERT INTO tiendamia_test (description, asin_code,price_amz, img, stock, weight, url, price,images) values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')"\
            .format(name,item[1],item[2],item[3],item[4],item[5],item[6], item[7], item[8])
        
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise

    def close(self):
        self.connection.close()


# open file in read mode
def get_file_records():
    records = []
    with open('test-result.csv', 'r', encoding='utf-8') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)    
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            # row variable is a list that represents a row in csv
            records.append(row)

    return records

def get_url(asin):
    """genera url"""
    template = 'https://tiendamia.com/ar/producto?amz={}'
    
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

#def main():
# conexion a base
database = DataBase()

# iniciar webdriver
driver  = webdriver.Chrome()

#cambio codificacion de caracteres
(driver.page_source).encode('utf-8')

records = get_file_records()

for record in records:
    asin = record[1]
    price_amz = record[2]
    img = record[3]


    url = get_url(asin)
    driver.get(url)        

    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    result = get_item(soup,url,price_amz,img,asin)        

    # guardar resultados
    if result:
        database.insert_item(result);
    else:
        print ('Error en:', asin)

database.close()
#driver.close()

#main()
