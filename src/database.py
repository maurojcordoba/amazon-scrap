import sqlite3
import re

class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect('data.db')    
        self.cursor = self.connection.cursor()      
        self.create_database()

    def create_database(self):
        sql = '''CREATE TABLE IF NOT EXISTS "amazon" (
                "id" INTEGER NOT NULL,
                "description" TEXT NULL DEFAULT '',
                "asin_code" VARCHAR(20) NULL DEFAULT '',
                "price" VARCHAR(25) NULL DEFAULT '',
                "img" TEXT NULL DEFAULT NULL,
                "url" TEXT NULL DEFAULT NULL,
                "on_bl" TINYINT NULL,
                "price_bl" VARCHAR(25) NULL DEFAULT NULL,
                PRIMARY KEY ("id")
                )'''
        self.cursor.execute(sql)
        self.connection.commit()
   
    def insert_item(self, item):
        name = self.connection.escape_string(item[0])
        sql = "INSERT INTO tiendamia (description, asin_code,price_amz, img, stock, weight, url, price,images) values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')"\
            .format(name,item[1],item[2],item[3],item[4],item[5],item[6], item[7], item[8])
        
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise
    
    def fav(self,id):
        
        try:
            sql = 'SELECT COUNT(*) FROM fav WHERE amazon_id = {}'.format(id)
            self.cursor.execute(sql)
            cur_result = self.cursor.fetchone()
            if(cur_result[0] != 0):
                sql = 'DELETE FROM fav WHERE amazon_id = {}'.format(id)
                self.cursor.execute(sql)
                self.connection.commit()
                return 0
            else:    
                sql = 'INSERT INTO fav (amazon_id) VALUES ({})'.format(id)
                self.cursor.execute(sql)
                self.connection.commit()
                return 1                
        except Exception as e:
            raise  

    def insert_fav(self, id):        
        sql = 'INSERT INTO fav (amazon_id) VALUES ({})'.format(id)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise  

    def delete_fav(self, id):        
        try:
            self.cursor.execute('DELETE fav WHERE amazon_id = ?', (id))
            self.connection.commit()
        except Exception as e:
            raise  
    
    def get_all_items(self):
        sql = 'SELECT * FROM amazon LIMIT 10'

        try:
            self.cursor.execute(sql);            
            items = [list(item) for item in self.cursor.fetchall()]

            return items
        except Exception as e:
            raise

    def get_bl_items(self):
        # sql = "SELECT * FROM amazon WHERE on_bl is 1 ORDER BY cast(replace(replace(price_bl,'$ ',''),'.','') AS INT) DESC;"
        sql = "SELECT * FROM amazon WHERE on_bl is 1 ORDER BY modified asc;"
        
        try:
            self.cursor.execute(sql);            
            items = [list(item) for item in self.cursor.fetchall()]

            return items
        except Exception as e:
            raise

    def get_tm_items(self):
        # sql = "SELECT * FROM amazon WHERE on_bl is 1 ORDER BY cast(replace(replace(price_bl,'$ ',''),'.','') AS INT) DESC;"
        sql = "SELECT * FROM amazon WHERE on_tm is 1 and stock_tm != 'Out of Stock' ORDER BY weigth asc LIMIT 5;"
        sql = """SELECT a.*, CASE WHEN b.amazon_id IS NULL THEN 0 ELSE 1 END as isfav
                FROM amazon a LEFT JOIN fav b
                on a.id = b.amazon_id
                WHERE a.on_tm is 1 and a.stock_tm != 'Out of Stock' 
                ORDER BY weigth asc;"""
        
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
    
    def insert_item(self, item):
        name = self.connection.escape_string(item[0])
        sql = "INSERT INTO amazon (description, asin_code,price_amz, img, stock, weight, url, price,images) values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')"\
            .format(name,item[1],item[2],item[3],item[4],item[5],item[6], item[7], item[8])
        
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise    
    
    def amazon_insert_item(self, item):
        name = item[0]        
        
        try:
            self.cursor.execute('INSERT INTO amazon (description, asin_code,price, img, url ) values (?,?,?,?,?)', (name,item[1],item[2],item[3],item[4]))            
            self.connection.commit()
        except Exception as e:
            raise    
    

    def amazon_get_items(self):        
        sql = "SELECT id,asin_code FROM amazon WHERE on_bl is null ORDER BY modified DESC"
        
        try:
            self.cursor.execute(sql)
            items = self.cursor.fetchall()
            results = []
            for item in items:
                results.append(item)

            return results

        except Exception as e:
            raise

    def amazon_get_items_tm(self):        
        # sql = "SELECT id,asin_code FROM amazon WHERE on_tm is null"
        sql = """SELECT id,asin_code FROM amazon 
                WHERE (on_tm is 1 OR on_bl = 1) 
                AND price_tm = '' AND STOCK_TM != 'Out of Stock'"""
        
        try:
            self.cursor.execute(sql)
            items = self.cursor.fetchall()
            results = []
            for item in items:
                results.append(item)

            return results

        except Exception as e:
            raise

    def amazon_update_item(self, on_bl,price_bl, id):                
        try:            
            updatedRow = self.cursor.execute('UPDATE amazon SET on_bl = ?, price_bl = ?, modified=datetime()  WHERE id = ?', (on_bl,price_bl,id)).rowcount                        
            self.connection.commit()            
            return updatedRow        
        except Exception as e:
            raise

    def amazon_update_item(self, on_tm,price_tm,stock_tm,weight_tm,url_tm, id):                
        try:            
            updatedRow = self.cursor.execute('UPDATE amazon SET on_tm = ?, price_tm = ?, stock_tm= ?,weigth= ?, url_tm=?, modified=datetime()  WHERE id = ?', (on_tm,price_tm,stock_tm,weight_tm,url_tm,id)).rowcount                        
            self.connection.commit()            
            return updatedRow        
        except Exception as e:
            raise

    def walmart_insert_item(self, item):
        description = self.connection.escape_string(item[0])
        sql = "INSERT INTO walmart (description, asin_code,price, img, url) values ('{0}','{1}','{2}','{3}','{4}')"\
            .format(description,item[1],item[2],item[3],item[4])
        
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise    

    def close(self):
        self.cursor.close()
        self.connection.close()