from flask import Flask, render_template,request
from flaskext.mysql import MySQL
from database import DataBase
import json

app = Flask(__name__)

@app.route('/')
def home():
    title = 'TiendaMia'
    
    url_template = 'https://tiendamia.com/ar/producto?amz={}'
        
    database = DataBase()
    items = database.get_tm_items()
    
    data = items 
    return render_template('tiendamia.html', data=data ,title=title,url_template=url_template) 
    
@app.route('/custom')
def custom():
    title = 'Custom'

    database = DataBase()
    items = database.get_custom_query()
    
    data = items    
    return render_template('custom.html', data=data ,title=title)
    
@app.route('/buscalibre')
def buscalibre():
    title = 'BuscaLibre'

    url_template = 'https://www.buscalibre.com.ar/amazon?url=https%3A%2F%2Fwww.amazon.com%2Fdp%2F{}&t=tetraemosv4'

    database = DataBase()
    items = database.get_bl_items()
    
    data = items 
    return render_template('buscalibre.html', data=data ,title=title,url_template=url_template) 

@app.route('/tiendamia')
def tiendamia():
    title = 'TiendaMia'
    
    url_template = 'https://tiendamia.com/ar/producto?amz={}'
        
    database = DataBase()
    items = database.get_tm_items()
    
    data = items 
    return render_template('tiendamia.html', data=data ,title=title,url_template=url_template) 

@app.route('/favorites/')
def favorites():    
    id = request.args.get('id')
    database = DataBase()
    result = database.fav(id)        
    return json.dumps({ "result": result})

@app.route('/favorites/remove')
def favorites_remove():    
    id = request.args.get('id')
    database = DataBase()
    database.delete_fav(id)
    
    return 'Ok'


@app.route('/about')
def about():
    return render_template('about.html')

def query_string():
    print(request)
    print(request.args)
    print(request.args.get('p1'))
    return 'Ok'

def pagina_no_encontrada(error):    
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.add_url_rule('/query_string',view_func=query_string)

    app.register_error_handler(404,pagina_no_encontrada)

    app.run(host='0.0.0.0', debug=True, port=5000)