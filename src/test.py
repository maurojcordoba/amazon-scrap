import pymysql;

class DataBase:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='insertcoin',
            db='scrap'
        )
    
        self.cursor = self.connection.cursor()

    def get_user(self,id):
        sql = 'SELECT * FROM users WHERE id = {0}'.format(id)

        try:
            self.cursor.execute(sql);
            user = self.cursor.fetchone()
            print ("id: ",user[0])
            print ("username: ",user[1])
            print ("email: ",user[2])

        except Exception as e:
            raise

    def get_all_users(self):
        sql = 'SELECT id,username,email FROM users'

        try:
            self.cursor.execute(sql);
            users = self.cursor.fetchall()
            for user in users:
                print ("id: ",user[0])
                print ("username: ",user[1])
                print ("email: ",user[2])
                print ("______ \n")

        except Exception as e:
            raise

    def update_user(self, id, username):
        sql = "UPDATE users SET username = '{}' WHERE id = {}".format(username,id)

        try:
            self.cursor.execute(sql);
        
        except Exception as e:
            raise

    def close(self):
        self.connection.close()
        
database = DataBase()
database.get_user(1);

database.close()
