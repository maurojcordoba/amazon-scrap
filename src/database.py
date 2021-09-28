import pymysql
import re

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
        sql = "INSERT INTO tiendamia (description, asin_code,price_amz, img, stock, weight, url, price,images) values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')"\
            .format(name,item[1],item[2],item[3],item[4],item[5],item[6], item[7], item[8])
        
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise
    
    def get_all_items(self):
        sql = 'SELECT * FROM tiendamia LIMIT 10'

        try:
            self.cursor.execute(sql);            
            items = [list(item) for item in self.cursor.fetchall()]

            return items
        except Exception as e:
            raise

    def get_bl_items(self):
        sql = "SELECT * FROM amazon WHERE on_bl is TRUE ORDER BY id DESC"

        try:
            self.cursor.execute(sql);            
            items = [list(item) for item in self.cursor.fetchall()]

            return items
        except Exception as e:
            raise

    def get_custom_query(self):
        sql = 'SELECT * FROM tiendamia_menos_1 WHERE weight < 1 ORDER BY diff desc, TOTAL_TM ASC limit 20'        

        try:
            self.cursor.execute(sql);            
            #items = [list(item) for item in self.cursor.fetchall()]
            
            items = []
            for item in self.cursor.fetchall():
                item =list(item)
                item[11] = re.sub('._AC_','.jpg',item[11])
                images_list = list(re.sub('["\[\]]','',item[11]).split(','))                
                item[11] = images_list
                items.append(item)

            return items
        except Exception as e:
            raise
        
    def close(self):
        self.connection.close()