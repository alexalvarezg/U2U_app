from . import app, db
from .models import Estudiante,EstudianteSchema
from flask import redirect, jsonify, make_response, request



@app.route("/")
def index_Detail():
    return "Bienvenido a la app de gestion"

@app.route("/about")
def about():
    return "All about Flask"




# a) MOSTRAR TODOS LOS Estudiantes
@app.route('/estudiantes', methods = ['GET'])
def index():
    get_estudiantes = Estudiante.query.all()
    estudiante_schema = EstudianteSchema(many=True)
    estudiantes = estudiante_schema.dump(get_estudiantes)
    return make_response(jsonify({"Estudiantes": estudiantes}))



# b) ELIMINAR UN PRODUCTO EN CONCRETO
@app.route('/estudiantes/delete/<id>')
def erase(id):
    '''
    Deletes the data on the basis of unique id and redirects to "home page"
    DUDA PORQUE NO LLEVA EL METHOD = 'DELETE'
    '''
    data = Estudiante.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/estudiantes')


# c) INCORPORAR UN ESTUDIANTE EN CONCRETO
@app.route('/estudiantes/add')
def create_student():
    '''
    Adds the data on the basis of unique id and redirects to "home page"
    '''
    estudiante = Estudiante(nombre="Alejandro" , apellidos="Alvarez Gallardo", curso=4, grado="GIT", titulo="InglesC1")
    print(estudiante)
    db.session.add(estudiante)
    db.session.commit()
    return redirect('/estudiantes')

''' funcion que tenian ellos para incorporar un nuevo prod
@app.route('/products', methods = ['POST'])
def create_product():
    data = request.get_json()
    product_schema = ProductSchema()
    product = product_schema.load(data)
    result = product_schema.dump(product.create())
    return make_response(jsonify({"product": result}),200)
'''


# d) MODIFICAR UN ESTUDIANTE EN CONCRETO ----------- SIN TERMINAR
@app.route('/products/update/<id>')
def update_product_by_id(id):
    '''
    Modifies a product and returns to "home Page"
    
    data = Estudiante.query.get(id)
    get_product = Estudiante.query.get(id)
    if data.get('title'):
        get_product.title = data['title']
    if data.get('productDescription'):
        get_product.productDescription = data['productDescription']
    if data.get('productBrand'):
        get_product.productBrand = data['productBrand']
    if data.get('price'):
        get_product.price= data['price']    
    db.session.add(get_product)
    db.session.commit()
    product_schema = ProductSchema(only=['id', 'title', 'productDescription','productBrand','price'])
    product = product_schema.dump(get_product)
    return make_response(jsonify({"product": product}))
    '''



# e) RUTA ALTERNATIVA PARA MOSTRAR TEXTO
@app.route('/rndm', methods = ['GET'])
def whatever():
    return make_response("se ha ejecutado correctamente")


@app.route('/postendpoint', methods = ['POST'])
def other():
    request_data = request.get_json()
    value1 = request_data['attr1']
    value2 = request_data['attr2']
