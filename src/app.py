from flask import Flask, render_template,request
from flaskext.mysql import MySQL
from database import DataBase
import json

app = Flask(__name__)

@app.route('/')
def home():
    title = 'Home'

    database = DataBase()
    items = database.get_all_items()
    
    data = items    
    return render_template('home.html', data=data ,title=title)
    
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

#app.route('/product/<id>')
#ef product(id):
#   try:
#       cant_dias = 15
#
#       # Busco ultima fecha cargada
#       producto_cur = mongo.db.productos.find({},{"created":1}).sort("created",-1).limit(1)
#       for p in producto_cur:
#           fec_ult_proc = p["created"]        
#       
#       # Muestro el ultimo producto cargado
#       producto_cur = mongo.db.productos.find({"id": id, "created": {"$eq":fec_ult_proc}}).sort("created",-1).limit(1)
#       for pp in producto_cur:
#           producto = pp
#
#       historial = mongo.db.productos.find({"id":id},{"price":1, "created":1}).sort("created", -1).limit(cant_dias)
#
#       data_chart = []
#       labels = []
#       for h in historial:        
#           data_chart.append(h['price'])
#           labels.append(h['created'].strftime('%d/%m/%y'))
#       
#       data_chart.reverse()
#       labels.reverse()
#
#       data = {
#           'title': 'Product',
#           'producto': producto,
#           'labels': labels,
#           'data_chart': data_chart,
#           'url_base': url_base,
#           'cant_dias': cant_dias
#       }
#       return render_template('product.html',data=data)
#   except pymongo.errors.ServerSelectionTimeoutError as e:
#       return "Error en Base de Datos %s" % e

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

    app.run(debug=True, port=5000)