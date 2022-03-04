from tkinter import E
from . import app, db
from .models import *
from flask import redirect, jsonify, make_response, request


@app.route("/")
def index_Detail():
    return "Bienvenido a la app de gestion de Erasmus"

@app.route("/about")
def about():
    return "All about Flask"


'''
ESTUDIANTES
'''

# A) GET: MOSTRAR TODOS LOS ESTUDIANTES
@app.route('/estudiantes', methods = ['GET'])
def index():
    get_estudiantes = Estudiante.query.all()
    estudiante_schema = EstudianteSchema(many=True)
    estudiantes = estudiante_schema.dump(get_estudiantes)
    return make_response(jsonify({"Estudiantes": estudiantes}))

# B.1) POST: INCORPORAR UN ESTUDIANTE
@app.route('/postendpoint/estudiante', methods = ['POST'])
def add_student():
    request_data = request.get_json()
    name = request_data['nombre']
    surname = request_data['apellidos']
    grade = request_data['curso']
    degree = request_data['grado']
    level = request_data['titulo']
    #print(name)
    #print(surname)
    #print(grade)
    #print(degree)
    #print(level)
    nuevo_estudiante = Estudiante(nombre=name , apellidos=surname, curso=grade, grado=degree, titulo=level)
    print(nuevo_estudiante)
    db.session.add(nuevo_estudiante)
    db.session.commit()

    return make_response(jsonify({"Status" : "Sudent added"}))

# B.2) POST: INCORPORAR VARIOS ESTUDIANTES
@app.route('/postendpoint/estudiantes', methods = ['POST'])
def add_students():
    request_data = request.get_json()
    print(request_data)
    for i in range(1, len(request_data)):
        name = request_data[i]['nombre']
        surname = request_data[i]['apellidos']
        grade = request_data[i]['curso']
        degree = request_data[i]['grado']
        level = request_data[i]['titulo']
        #print(name)
        #print(surname)
        #print(grade)
        #print(degree)
        #print(level)
        nuevo_estudiante = Estudiante(nombre=name , apellidos=surname, curso=grade, grado=degree, titulo=level)
        print(nuevo_estudiante)
        db.session.add(nuevo_estudiante)
        db.session.commit()

    return make_response(jsonify({"Status" : "Various Students added"}))

# C.1) DELETE: ELIMINAR UN ESTUDIANTE EN CONCRETO DESDE POSTMAN
@app.route('/deleteendpoint', methods=['DELETE'])
def erase_student():
    request_data = request.get_json()
    print(request_data)
    surname_to_erase = request_data["apellidos"]
    print(surname_to_erase)
    
    db.session.query(Estudiante).filter(Estudiante.apellidos == surname_to_erase).delete(synchronize_session=False)
    db.session.commit()
    return redirect('/estudiantes')

# C.2) DELETE: ELIMINAR UN ESTUDIANTE EN CONCRETO DESDE NAVEGADOR INDICANDO ID
@app.route('/estudiantes/delete/<id>', methods=["DELETE"])
def erase_student_id(id):
    '''
    Deletes the data on the basis of unique id and redirects to "home page"
    DUDA PORQUE NO LLEVA EL METHOD = 'DELETE'
    '''
    data = Estudiante.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return "Estdudiante eliminado"


# C.3) DELETE: ELIMINAR TODOS LOS CUANTOS ESTUDIANTES 
@app.route('/deleteAllStudents', methods=["DELETE"])
def erase_all_students():
    get_estudiantes = Estudiante.query.all()
    print("\n Los estudiantes actuales son: \n")
    print(get_estudiantes)
    print("\n")
    for i in get_estudiantes:
        print("Estudiante que se va a eliminar: " + str(i))
        db.session.delete(i)
        db.session.commit()
        print(get_estudiantes)
    
    return make_response(jsonify({"Status" : "All students erased"}))



### ---------------------------------------------------------------------------------------

@app.route('/postestudiante', methods = ['POST'])
def other():
    request_data = request.get_json()
    print(request_data)
    
    value1 = request_data['attr1']
    value2 = request_data['attr2']
    print(value1)
    print(value2)

    return make_response(jsonify({"Status" : "student added"}))


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





'''
import requests
r = requests.post('127.0.0.1:5000/postendpoint', json={
"Id": 78912,
"Customer": "Jason Sweet",
"Quantity": 1,
"Price": 18.00
})
print(f"Status Code: {r.status_code}, Response: {r.json()}")

def create_product():
    data = request.get_json()
    student_schema = EstudianteSchema()
    estudiante = student_schema.load(data)
    result = student_schema.dump(estudiante.create())
    return make_response(jsonify({"Estudiante": result}),200)
'''

''' funcion que tenian ellos para incorporar un nuevo prod
@app.route('/products', methods = ['POST'])
def create_product():
    data = request.get_json()
    product_schema = ProductSchema()
    product = product_schema.load(data)
    result = product_schema.dump(product.create())
    return make_response(jsonify({"product": result}),200)


    # E) ELIMINAR UN ESTUDIANTE EN CONCRETO
    @app.route('/estudiantes/delete/<id>')
    def erase(id):

    #Deletes the data on the basis of unique id and redirects to "home page"
    #DUDA PORQUE NO LLEVA EL METHOD = 'DELETE'

    data = Estudiante.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/estudiantes')

'''





'''
ASIGNATURA DE ORIGEN
'''

# A) GET: MOSTRAR TODAS LAS ASIGNATURAS DE ORIGEN 
@app.route('/asignaturas_origen', methods = ['GET'])
def subjects():
    get_asignaturas = Asignatura_Origen.query.all()
    AsignaturaOrigen_schema = Asignatura_OrigenSchema(many=True)
    asignaturas = AsignaturaOrigen_schema.dump(get_asignaturas)
    return make_response(jsonify({"Asingaturas de Origen": asignaturas}))

# B.1) POST: INCORPORAR UNA ASIGNATURA
@app.route('/postendpoint/asignatura_origen', methods = ['POST'])
def add_subject():
    request_data = request.get_json()
    name = request_data['nombre']
    nueva_asignatura = Asignatura_Origen(nombre=name)
    db.session.add(nueva_asignatura)
    db.session.commit()

    return make_response(jsonify({"Status" : "Asignatura de origen added"}))

# B.2) POST: INCORPORAR VARIAS ASIGNATURAS DE ORIGEN
@app.route('/postendpoint/asignaturas_origen', methods = ['POST'])
def add_subjects():
    request_data = request.get_json()
    print(request_data)
    for i in range(1, len(request_data)):
        name = request_data[i]['nombre']
        #print(name)
        nueva_asignatura = Asignatura_Origen(nombre=name)
        db.session.add(nueva_asignatura)
        db.session.commit()

    return make_response(jsonify({"Status" : "Various Subjects added"}))


# C.3) DELETE: ELIMINAR TODAS LAS ASIGNATURAS DE ORIGEN 
@app.route('/deleteAllAsignaturasOrigen', methods=["DELETE"])
def erase_all_originsubjects():
    get_asignaturas = Asignatura_Origen.query.all()
    print("\n Las asignaturas de origen actuales son: \n")
    print(get_asignaturas)
    print("\n")
    for i in get_asignaturas:
        print("Asignaturas que se va a eliminar: " + str(i))
        db.session.delete(i)
        db.session.commit()
    
    return make_response(jsonify({"Status" : "All Subjects erased"}))



'''
ASIGNATURA DE DESTINO
'''

# A) GET: MOSTRAR TODAS LAS ASIGNATURAS DE DESTINO 
@app.route('/asignaturas_destino', methods = ['GET'])
def subjects_aborad():
    get_asignaturas = Asignatura_Destino.query.all()
    AsignaturaDestino_schema = Asignatura_DestinoSchema(many=True)
    asignaturas = AsignaturaDestino_schema.dump(get_asignaturas)
    return make_response(jsonify({"Asingaturas de Destino": asignaturas}))

# B.1) POST: INCORPORAR UNA ASIGNATURA DE DESTINO
@app.route('/postendpoint/asignatura_destino', methods = ['POST'])
def add_subject_abroad():
    request_data = request.get_json()
    name = request_data['nombre']
    nueva_asignatura = Asignatura_Destino(nombre=name)
    db.session.add(nueva_asignatura)
    db.session.commit()

    return make_response(jsonify({"Status" : "Asignatura de destino added"}))

# B.2) POST: INCORPORAR VARIAS ASIGNATURAS DE DESTINO
@app.route('/postendpoint/asignaturas_destino', methods = ['POST'])
def add_subjects_abroad():
    request_data = request.get_json()
    print(request_data)
    for i in range(1, len(request_data)):
        name = request_data[i]['nombre']
        #print(name)
        nueva_asignatura = Asignatura_Destino(nombre=name)
        db.session.add(nueva_asignatura)
        db.session.commit()

    return make_response(jsonify({"Status" : "Various Subjects added"}))

# C.3) DELETE: ELIMINAR TODAS LAS ASIGNATURAS DE DESTINO 
@app.route('/deleteAllAsignaturasDestino', methods=["DELETE"])
def erase_all_aboradsubjects():
    get_asignaturas = Asignatura_Destino.query.all()
    print("\n Las asignaturas de destino actuales son: \n")
    print(get_asignaturas)
    print("\n")
    for i in get_asignaturas:
        print("Asignaturas que se va a eliminar: " + str(i))
        db.session.delete(i)
        db.session.commit()
    
    return make_response(jsonify({"Status" : "All Subjects erased"}))



'''
UNIVERSIDAD
'''
# A) GET: MOSTRAR TODAS LAS UNIVERSIDADES 
@app.route('/universidad', methods = ['GET'])
def universityd():
    get_universidades = Universidad.query.all()
    Universidad_schema = UniversidadSchema(many=True)
    universidades = Universidad_schema.dump(get_universidades)
    return make_response(jsonify({"Universidad": universidades}))

# B.1) POST: INCORPORAR UNA UNIVERSIDAD
@app.route('/postendpoint/universidad', methods = ['POST'])
def add_university():
    request_data = request.get_json()
    name = request_data['nombre']
    place = request_data["ubicacion"]
    spots = request_data["plazas"]
    subject_id = request_data["id_asignatura_d"]
    nueva_universidad = Universidad(nombre=name, ubicacion=place, plazas=spots, id_asignatura_d=subject_id)
    print("nueva universidad añadida \n")
    print(nueva_universidad)
    db.session.add(nueva_universidad)
    db.session.commit()

    return make_response(jsonify({"Status" : "Universidad added"}))

# B.2) POST: INCORPORAR VARIAS UNIVERSIDADES
@app.route('/postendpoint/universidades', methods = ['POST'])
def add_universities():
    request_data = request.get_json()
    print(request_data)
    for i in range(1, len(request_data)):
        name = request_data[i]['nombre']
        place = request_data[i]["ubicacion"]
        spots = request_data[i]["plazas"]
        subject_id = request_data[i]["id_asignatura_d"]
        nueva_universidad = Universidad(nombre=name, ubicacion=place, plazas=spots, id_asignatura_d=subject_id)
        print("nueva universidad añadida \n")
        print(nueva_universidad)
        db.session.add(nueva_universidad)
        db.session.commit()

    return make_response(jsonify({"Status" : "Varias Universidades Añadidas"}))


# C.3) DELETE: ELIMINAR TODAS LAS UNIVERSIDADES 
@app.route('/deleteAllUniversidades', methods=["DELETE"])
def erase_all_universities():
    get_universidades = Universidad.query.all()
    print("\n Las Universsidades actuales son: \n")
    print(get_universidades)
    print("\n")
    for i in get_universidades:
        print("Universidades que se va a eliminar: " + str(i))
        db.session.delete(i)
        db.session.commit()
    
    return make_response(jsonify({"Status" : "All Universities erased"}))



'''
LEARNING AGREEMENT
'''
# A) GET: MOSTRAR TODOS LOS LA 
@app.route('/LA', methods = ['GET'])
def learnignAgreement():
    get_LA = LA.query.all()
    LA_schema = LASchema(many=True)
    Learning_agreement = LA_schema.dump(get_LA)
    return make_response(jsonify({"Learning Agreement": Learning_agreement}))

# B.1) POST: INCORPORAR UN LA
@app.route('/postendpoint/LA', methods = ['POST'])
def add_LA():
    request_data = request.get_json()
    student_id = request_data['id_estudiante']
    RRII_accept = request_data["aceptado_RRII"]
    coord_accept = request_data["aceptado_Coord"]
    RRII_sign = request_data["fdo_RRII"]
    coord_sign = request_data["fdo_Coord"]

    nuevo_LA = LA(id_estudiante=student_id, aceptado_RRII=RRII_accept, aceptado_Coord=coord_accept, fdo_RRII=RRII_sign, fdo_Coord=coord_sign)
    print("nuevo LA añadido \n")
    print(nuevo_LA)
    db.session.add(nuevo_LA)
    db.session.commit()

    return make_response(jsonify({"Status" : "LA added"}))

# B.2) POST: INCORPORAR VARIOS LA
@app.route('/postendpoint/LAs', methods = ['POST'])
def add_LAs():
    request_data = request.get_json()
    print(request_data)
    for i in range(1, len(request_data)):
        student_id = request_data[i]['id_estudiante']
        RRII_accept = request_data[i]["aceptado_RRII"]
        coord_accept = request_data[i]["aceptado_Coord"]
        RRII_sign = request_data[i]["fdo_RRII"]
        coord_sign = request_data[i]["fdo_Coord"]

        nuevo_LA = LA(id_estudiante=student_id, aceptado_RRII=RRII_accept, aceptado_Coord=coord_accept, fdo_RRII=RRII_sign, fdo_Coord=coord_sign)
        print("nuevos LA añadidos \n")
        print(nuevo_LA)
        db.session.add(nuevo_LA)
        db.session.commit()

    return make_response(jsonify({"Status" : "Varios LA Añadidos"}))

# C.3) DELETE: ELIMINAR TODOS LOS LA 
@app.route('/deleteAllLAs', methods=["DELETE"])
def erase_all_LAs():
    get_LAs = LA.query.all()
    print("\n Los LA disponibles son: \n")
    print(get_LAs)
    print("\n")
    for i in get_LAs:
        print("LAs que se va a eliminar: " + str(i))
        db.session.delete(i)
        db.session.commit()
    
    return make_response(jsonify({"Status" : "All LAs erased"}))



'''
        ASIGNATURA_DESTINO_ASIGNATURA_ORIGEN - no consigo que funcione
'''

# B.1) POST: INCORPORAR UN CONJUNTO DE ASIGNATURA DESTINO Y ORIGEN
@app.route('/postendpoint/Asignaturas_destino_origen', methods = ['POST'])
def add_origin_and_destiny_subject():
    request_data = request.get_json()
    origin_subject_id = request_data["id_asignatura_origen"]
    destiny_subject_id = request_data["id_asignatura_destino"]

    nuevas_asignaturas = Asignatura_Destino_Asignatura_Origen(id_asignatura_destino=destiny_subject_id, id_asignatura_origen=origin_subject_id,)
    print("nuevo AOD añadido \n")
    print(nuevas_asignaturas)
    db.session.add(nuevas_asignaturas)
    db.session.commit()

    return make_response(jsonify({"Status" : "AOD added"}))



'''
SELECCION 
'''

# A) GET: MOSTRAR TODAS LAS SELECCIONES
@app.route('/Seleccion', methods = ['GET'])
def Selection():
    get_Seleccion = Seleccion.query.all()
    Selection_schema = SeleccionSchema(many=True)
    seleccion = Selection_schema.dump(get_Seleccion)
    return make_response(jsonify({"Seleccion(es)": seleccion}))


# B.1) POST: INCORPORAR UNA SELECCION
@app.route('/postendpoint/seleccion', methods = ['POST'])
def add_selection():
    request_data = request.get_json()
    term = request_data['cuatri']
    year = request_data["año"]
    round = request_data["vuelta"]
    confirmation = request_data["confirmacion"]
    nueva_seleccion = Seleccion(cuatri=term, año=year, vuelta=round, confirmacion=confirmation) 
    print("nueva seleccion añadida \n")
    print(nueva_seleccion)
    db.session.add(nueva_seleccion)
    db.session.commit()

    return make_response(jsonify({"Status" : "Selection added"}))

# B.2) POST: INCORPORAR VARIAS SELECCIONES
@app.route('/postendpoint/selecciones', methods = ['POST'])
def add_selecciones():
    request_data = request.get_json()
    print(request_data)
    for i in range(1, len(request_data)):
        term = request_data[i]['cuatri']
        year = request_data[i]["año"]
        round = request_data[i]["vuelta"]
        confirmation = request_data[i]["confirmacion"]
        nueva_seleccion = Seleccion(cuatri=term, año=year, vuelta=round, confirmacion=confirmation) 
        print("nueva seleccion añadida \n")
        print(nueva_seleccion)
        db.session.add(nueva_seleccion)
        db.session.commit()

    return make_response(jsonify({"Status" : "Varias Selecciones Añadidas"}))

# C.3) DELETE: ELIMINAR TODOS LAS SELECCIONES  
@app.route('/deleteAllSelecciones', methods=["DELETE"])
def erase_all_selections():
    get_selections = Seleccion.query.all()
    print("\n Las Selecciones disponibles son: \n")
    print(get_selections)
    print("\n")
    for i in get_selections:
        print("Selecciones que se van a eliminar: " + str(i))
        db.session.delete(i)
        db.session.commit()
    
    return make_response(jsonify({"Status" : "All Selections erased"}))


'''
SELECCION - UNIVERSIDAD
'''

# A) GET: MOSTRAR TODAS LAS SELECCIONES-UNIVERSIDAD
@app.route('/Seleccion-Universidad', methods = ['GET'])
def Selection_University():
    get_selection_university = Seleccion_Universidad.query.all()
    selection_university_schema = Seleccion_UniversidadSchema(many=True)
    selection_university = selection_university_schema.dump(get_selection_university)
    return make_response(jsonify({"Seleccion(es)-Universidad(es)": selection_university}))

# B.1) POST: INCORPORAR UNA SELECCION
@app.route('/postendpoint/seleccion-universidad', methods = ['POST'])
def add_selection_university():
    request_data = request.get_json()
    university_id = request_data['id_universidad']
    selection_id = request_data["id_seleccion"]
    
    nueva_seleccion_uni = Seleccion_Universidad(id_universidad=university_id, id_seleccion=selection_id)  
    print("nueva seleccion-universidad añadida \n")
    print(nueva_seleccion_uni)
    db.session.add(nueva_seleccion_uni)
    db.session.commit()

    return make_response(jsonify({"Status" : "Selection-University added"}))