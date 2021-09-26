import csv
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from selenium import webdriver

def get_url(search_term):
    """genera url"""
    template = 'https://www.amazon.com/s?k={}&i=toys-and-games'
    search_term = search_term.replace(' ','+')

    url = template.format(search_term)

    url += '&page={}'

    return url

def extract_record(item):
    """Extraer el item"""

    # descripcion 
    atag = item.h2.a
    description = atag.text.strip()

    # asin codigo
    asin = item.get('data-asin')
    
    # url
    url = 'https://www.amazon.com' + atag.get('href')

    # precio
    try:
        price_parent = item.find('span','a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return

    # img
    try:
        img_parent = item.find('img','s-image')
        img = img_parent.get('src')
    except AttributeError:
        return

    result = (description,asin,price,img,url)

    return result

def main(search_term):
    # iniciar webdriver
    driver  = webdriver.Chrome()

    #cambio codificacion de caracteres
    (driver.page_source).encode('utf-8')
    
    records = []
    url = get_url(search_term)
    
    for page in range(1,400):
       driver.get(url.format(page))          
       soup = BeautifulSoup(driver.page_source, 'html.parser')
       results = soup.find_all('div',{'data-component-type': 's-search-result'})

       for item in results:
           record = extract_record(item)
           if record:
               records.append(record)

    driver.close()


    # guardar resultados
    with open('result.csv','w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f,delimiter=',')
        # writer.writerow(['Descripcion', 'ASIN', 'Precio', 'URL'])
        writer.writerows(records)

main('board games')

