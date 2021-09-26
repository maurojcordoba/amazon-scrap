
from typing import Annotated
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import sessionmaker
from csv import reader

engine = create_engine('mysql+pymysql://root:insertcoin@localhost/scrap')
Base = declarative_base()

class Amazon(Base):
    __tablename__ = 'amazon'

    id = Column(Integer(), primary_key=True)
    description = Column(Text(), nullable=True)
    asin_code = Column(String(15), nullable=True)
    price = Column(String(25), nullable=True)
    img = Column(String(255), nullable=True)
    url = Column(String(255), nullable=True)

    def __str__(self):
        return self.description

Session = sessionmaker(engine)
session = Session()

# open file in read mode
def get_file_records():
    records = []
    with open('../result.csv', 'r', encoding='utf-8') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)    
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            # row variable is a list that represents a row in csv
            records.append(row)

    return records


if __name__ == '__main__':
    

    # Borrar registro de la tabla
    #session.query(Amazon).delete()
    #session.commit()

    # Obtener datos de tabla
    #results  = session.query(Amazon).all()

    #item = Amazon(description='description',asin_code='BA6565S',price='US$23.49')
    #session.add(item)

    #results = get_file_records()
    #for i in results :        
    #    item = Amazon(description=i[0],asin_code=i[1],price=i[2],img=i[3], url=i[4])        
    #    session.add(item)

    #session.commit()

    x = session.query(Amazon).get(837)
    print(x.name)