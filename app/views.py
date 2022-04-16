from tkinter import E
from . import app, db
from .models import *
from flask import redirect, jsonify, make_response, render_template, request
from flask import render_template
from sqlalchemy import text




@app.route("/")
def index_prueba():
    return render_template("index.html")

@app.route("/.")
def index_Detail():
    return "Bienvenido a la app de gestion de Erasmus"

@app.route("/about")
def about():
    return "All about Flask"

'''
QUERIES
'''

@app.route("/estudiantes")
def select_estudiantes():
    output = db.engine.execute('SELECT * FROM estudiantes;').fetchall()
    return render_template('Estudiantes.html',result=output)
    
@app.route("/estudiantes_con_idiomas")
def select_estudiantes_idiomas():
    output = db.engine.execute('SELECT E.id, nombre, apellidos, curso, grado, idioma, nivel FROM estudiantes E, titulo T, aux_titulo_estudiante A WHERE E.id=A.id_estudiante AND T.id = A.id_titulo ORDER BY E.id;').fetchall()
    return render_template('Estudiantes_idiomas.html',result=output)
    
@app.route("/universidades")
def select_universidades():
    output = db.engine.execute('SELECT * FROM universidad;').fetchall()
    return render_template('Universidad.html',result=output)


@app.route("/universidades_con_idiomas")
def select_universidades_idiomas():
    output = db.engine.execute('SELECT U.id, nombre, ubicacion, plazas, idioma, nivel FROM universidad U, titulo T, aux_titulo_universidad A WHERE U.id=A.id_universidad AND T.id = A.id_titulo ORDER BY U.id;').fetchall()
    return render_template('Universidad_idiomas.html',result=output)


@app.route("/titulos")
def select_titulos():
    output = db.engine.execute('SELECT * FROM titulo ORDER BY id;').fetchall()
    return render_template('Titulos.html',result=output)


@app.route("/asignaturasOrigen")
def select_asignaturasO():
    output = db.engine.execute('SELECT * FROM asignatura_origen;').fetchall()
    return render_template('AsignaturasOrigen.html',result=output)

@app.route("/asignaturasDestino")
def select_asignaturasD():
    output = db.engine.execute('SELECT * FROM asignatura_destino;').fetchall()
    return render_template('AsignaturasDestino.html',result=output)

@app.route("/asignaturasDestinoOrigen")
def select_asignaturasOD():
    output = db.engine.execute('SELECT OD.id, O.nombre, D.nombre FROM asignatura_origen O, asignatura_destino D, asignatura_destino_asignatura_origen OD WHERE O.id = OD.id_asignatura_origen AND D.id = OD.id_asignatura_destino;').fetchall()
    return render_template('AsignaturasDestinoOrigen.html',result=output)


@app.route("/seleccion")
def select_selection():
    output = db.engine.execute('SELECT E.id, E.nombre, E.apellidos, E.curso, E.grado, S.año, S.cuatri, S.vuelta, U.nombre FROM estudiantes E, seleccion S, aux_estudiante_seleccion A, universidad U WHERE E.id=A.id_estudiante AND S.id=A.id_seleccion AND U.id=S.confirmacion;').fetchall()
    return render_template('Seleccion.html',result=output)



'''
TITULO
'''

# A) GET: MOSTRAR TODOS LOS TITULOS
@app.route('/titulos', methods = ['GET'])
def see_titulos():
    get_titulos = Titulo.query.all()
    titulo_schema = Titulo_Schema(many=True)
    titulos = titulo_schema.dump(get_titulos)
    return make_response(jsonify({"Titulo(s)": titulos}))


# B.1) POST: INCORPORAR UN TITULO
@app.route('/postendpoint/titulo', methods = ['POST'])
def add_titulo():
    request_data = request.get_json()
    language = request_data['idioma']
    level = request_data['nivel']
    
    nuevo_titulo = Titulo(idioma=language , nivel=level) 
    #print(nuevo_titulo)
    db.session.add(nuevo_titulo)
    db.session.commit()
    return make_response(jsonify({"Status" : "Titulo added"}))

# B.2) POST: INCORPORAR VARIOS TITULOS
@app.route('/postendpoint/titulos', methods = ['POST'])
def add_titulos():
    request_data = request.get_json()
    #print(request_data)
    for i in range(0, len(request_data)):
        language = request_data[i]['idioma']
        level = request_data[i]['nivel']
        nuevo_titulo = Titulo(idioma=language , nivel=level) 
        #print(nuevo_estudiante)
        db.session.add(nuevo_titulo)
        db.session.commit()
    return make_response(jsonify({"Status" : "Various Titulos added"}))



'''
ESTUDIANTES
'''

# A) GET: MOSTRAR TODOS LOS ESTUDIANTES
@app.route('/estudiantes', methods = ['GET'])
def index():
    get_estudiantes = Estudiante.query.all()
    estudiante_schema = EstudianteSchema(many=True)
    estudiantes = estudiante_schema.dump(get_estudiantes)
    # Estudiantes should have the object titles
    return make_response(jsonify({"Estudiantes": estudiantes}))
    #return render_template('estudiantes.html', data=estudiantes)

# B.1) POST: INCORPORAR UN ESTUDIANTE
@app.route('/postendpoint/estudiante', methods = ['POST'])
def add_student():
    request_data = request.get_json()
    name = request_data['nombre']
    surname = request_data['apellidos']
    grade = request_data['curso']
    degree = request_data['grado']
    #title = request_data["titulo"]
    print("**************************")
    if "titulo" in request_data:
        print("si hay titulo")
        titles = request_data["titulo"]
        print(titles)
        # For ID in titles
        query_1 = db.session.query(Titulo).filter(Titulo.id == titles)
        #Resultado de query_1 con titulos (objetos de tipo titulo)

        nuevo_estudiante = Estudiante(nombre=name , apellidos=surname, curso=grade, grado=degree, titulo=query_1)
        print(nuevo_estudiante.titulo)
        
    else: 
        print("heeey")
        nuevo_estudiante = Estudiante(nombre=name , apellidos=surname, curso=grade, grado=degree, titulo=[])
    #print(nuevo_estudiante)
    db.session.add(nuevo_estudiante)
    db.session.commit()
    return make_response(jsonify({"Status" : "Sudent added"}))


# (B.1_PRUEBA) POST: INCORPORAR UN ESTUDIANTE FORMULARIO
@app.route('/estudiante_form', methods = ['GET','POST'])
def add_student_form():
    if request.method == "POST":
        # getting input with name = fname in HTML form
       name = request.form.get("name")
       # getting input with name = lname in HTML form 
       surname = request.form.get("surname") 
       grade = request.form.get("grade") 
       degree = request.form.get("degree") 
       
       try:
           title = request.form.get("title")
           query_1 = db.session.query(Titulo).filter(Titulo.id == title)
           nuevo_estudiante = Estudiante(nombre=name , apellidos=surname, curso=grade, grado=degree, titulo=query_1)
        #    db.session.add(nuevo_estudiante)
        #    db.session.commit()
       except:
           nuevo_estudiante = Estudiante(nombre=name , apellidos=surname, curso=grade, grado=degree, titulo=[])
        #    db.session.add(nuevo_estudiante)
        #    db.session.commit()
       
       db.session.add(nuevo_estudiante)
       db.session.commit()
       get_estudiantes = Estudiante.query.all()
       estudiante_schema = EstudianteSchema(many=True)
       estudiantes = estudiante_schema.dump(get_estudiantes)
        # Estudiantes should have the object titles
       output = db.engine.execute('SELECT * FROM estudiantes;').fetchall()
       return render_template('Estudiantes.html',result=output)
       #return make_response(jsonify({"Estudiantes": estudiantes}))

    return render_template("formulario_estudiante.html")



# B.2) POST: INCORPORAR VARIOS ESTUDIANTES
@app.route('/postendpoint/estudiantes', methods = ['POST'])
def add_students():
    request_data = request.get_json()
    #print(request_data)
    for i in range(0, len(request_data)):
        name = request_data[i]['nombre']
        surname = request_data[i]['apellidos']
        grade = request_data[i]['curso']
        degree = request_data[i]['grado']
        if "titulo" in request_data[i]:
            #print("si esta")
            title = request_data[i]['titulo'][0]
            #print(title)
            query_1 = db.session.query(Titulo).filter(Titulo.id == title)
            nuevo_estudiante = Estudiante(nombre=name , apellidos=surname, curso=grade, grado=degree, titulo=query_1)
            print("Estudiante incorporado CON titulo")
        else:
            #print("no esta")
            nuevo_estudiante = Estudiante(nombre=name , apellidos=surname, curso=grade, grado=degree, titulo=[])
            print("Estudiante incorporado SIN titulo")
        db.session.add(nuevo_estudiante)
        db.session.commit()
    return make_response(jsonify({"Status" : "Various Students added"}))

'''
# B.2) POST: INCORPORAR VARIOS ESTUDIANTES
@app.route('/postendpoint/estudiantes', methods = ['POST'])
def add_students():
    request_data = request.get_json()
    #print(request_data)
    for i in range(0, len(request_data)):
        name = request_data[i]['nombre']
        surname = request_data[i]['apellidos']
        grade = request_data[i]['curso']
        degree = request_data[i]['grado']
        title = request_data[i]['titulo']
        query_1 = db.session.query(Titulo).filter(Titulo.id == title)
        nuevo_estudiante = Estudiante(nombre=name , apellidos=surname, curso=grade, grado=degree, titulo=query_1)
        #print(nuevo_estudiante)
        db.session.add(nuevo_estudiante)
        db.session.commit()
    return make_response(jsonify({"Status" : "Various Students added"}))
'''

# C.1) DELETE: ELIMINAR UN ESTUDIANTE EN CONCRETO DESDE POSTMAN
@app.route('/deleteendpoint', methods=['DELETE'])
def erase_student():
    request_data = request.get_json()
    #print(request_data)
    surname_to_erase = request_data["apellidos"]
    #print(surname_to_erase) 
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
    return "Estudiante eliminado"


# C.3) DELETE: ELIMINAR TODOS LOS CUANTOS ESTUDIANTES 
@app.route('/deleteAllStudents', methods=["DELETE"])
def erase_all_students():
    get_estudiantes = Estudiante.query.all()
    print("\n Los estudiantes actuales son: \n")
    #print(get_estudiantes)
    #print("\n")
    for i in get_estudiantes:
        #print("Estudiante que se va a eliminar: " + str(i))
        db.session.delete(i)
        db.session.commit()
        #print(get_estudiantes)
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
    #print(request_data)
    for i in range(0, len(request_data)):
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
    #print("\n Las asignaturas de origen actuales son: \n")
    #print(get_asignaturas)
    #print("\n")
    for i in get_asignaturas:
        #print("Asignaturas que se va a eliminar: " + str(i))
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
    university_id = request_data['id_universidad']
    nueva_asignatura = Asignatura_Destino(nombre=name, id_universidad=university_id)
    db.session.add(nueva_asignatura)
    db.session.commit()
    return make_response(jsonify({"Status" : "Asignatura de destino added"}))

# B.2) POST: INCORPORAR VARIAS ASIGNATURAS DE DESTINO
@app.route('/postendpoint/asignaturas_destino', methods = ['POST'])
def add_subjects_abroad():
    request_data = request.get_json()
    #print(request_data)
    for i in range(0, len(request_data)):
        name = request_data[i]['nombre']
        university_id = request_data[i]['id_universidad']
        #print(name)
        nueva_asignatura = Asignatura_Destino(nombre=name, id_universidad=university_id)
        db.session.add(nueva_asignatura)
        db.session.commit()
    return make_response(jsonify({"Status" : "Various Subjects added"}))

# C.3) DELETE: ELIMINAR TODAS LAS ASIGNATURAS DE DESTINO 
@app.route('/deleteAllAsignaturasDestino', methods=["DELETE"])
def erase_all_aboradsubjects():
    get_asignaturas = Asignatura_Destino.query.all()
    #print("\n Las asignaturas de destino actuales son: \n")
    #print(get_asignaturas)
    #print("\n")
    for i in get_asignaturas:
        #print("Asignaturas que se va a eliminar: " + str(i))
        db.session.delete(i)
        db.session.commit()
    return make_response(jsonify({"Status" : "All Subjects erased"}))



'''
UNIVERSIDAD
'''
# A) GET: MOSTRAR TODAS LAS UNIVERSIDADES 
@app.route('/universidad', methods = ['GET'])
def university():
    get_universidades = Universidad.query.all()
    Universidad_schema = UniversidadSchema(many=True)
    universidades = Universidad_schema.dump(get_universidades)
    return make_response(jsonify({"Universidad": universidades}))

# B.1) POST: INCORPORAR UNA UNIVERSIDAD
@app.route('/postendpoint/universidad', methods = ['GET', 'POST'])
def add_university():
    request_data = request.get_json()
    name = request_data['nombre']
    place = request_data["ubicacion"]
    spots = request_data["plazas"]
    if "titulo" in request_data:
        title = request_data["titulo"][0]
        query_1 = db.session.query(Titulo).filter(Titulo.id == title)
        nueva_universidad = Universidad(nombre=name, ubicacion=place, plazas=spots, titulo=query_1)
    else:
        nueva_universidad = Universidad(nombre=name, ubicacion=place, plazas=spots, titulo=[]) 

    db.session.add(nueva_universidad)
    db.session.commit()

    return make_response(jsonify({"Status" : "Universidad added"}))

# B.2) POST: INCORPORAR VARIAS UNIVERSIDADES
@app.route('/postendpoint/universidades', methods = ['POST'])
def add_universities():
    request_data = request.get_json()
    #print(request_data)
    for i in range(0, len(request_data)):
        name = request_data[i]['nombre']
        place = request_data[i]["ubicacion"]
        spots = request_data[i]["plazas"]
        if "titulo" in request_data[i]:
            title = request_data[i]["titulo"]
            query_1 = db.session.query(Titulo).filter(Titulo.id == title)
            nueva_universidad = Universidad(nombre=name, ubicacion=place, plazas=spots,  titulo=query_1 )
        else:
            nueva_universidad = Universidad(nombre=name, ubicacion=place, plazas=spots,  titulo=[])
        #print("nueva universidad añadida \n")
        #print(nueva_universidad)
        db.session.add(nueva_universidad)
        db.session.commit()
    return make_response(jsonify({"Status" : "Varias Universidades Añadidas"}))


# C.3) DELETE: ELIMINAR TODAS LAS UNIVERSIDADES 
@app.route('/deleteAllUniversidades', methods=["DELETE"])
def erase_all_universities():
    get_universidades = Universidad.query.all()
    #print("\n Las Universsidades actuales son: \n")
    #print(get_universidades)
    #print("\n")
    for i in get_universidades:
        #print("Universidades que se va a eliminar: " + str(i))
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
    #print(get_LA) #shows __repr__ de LA
    LA_schema = LASchema(many=True)
    Learning_agreement = LA_schema.dump(get_LA)
    #print(LA_schema.dump_fields)
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
    if "listado_asignaturasOD" in request_data:
        listado = request_data["listado_asignaturasOD"]
        for i in range(0, len(listado)):
            asignaturas_id = listado[i]
            query_1 = db.session.query(Asignatura_Destino_Asignatura_Origen).filter(Asignatura_Destino_Asignatura_Origen.id == asignaturas_id)
            nuevo_LA = LA(id_estudiante=student_id, aceptado_RRII=RRII_accept, aceptado_Coord=coord_accept, fdo_RRII=RRII_sign, fdo_Coord=coord_sign, listado_asignaturasOD=query_1)
            print("incorporado LA con asignaturas OD")
    #print("nuevo LA añadido \n")
    #print(nuevo_LA)
    else: 
        nuevo_LA = LA(id_estudiante=student_id, aceptado_RRII=RRII_accept, aceptado_Coord=coord_accept, fdo_RRII=RRII_sign, fdo_Coord=coord_sign, listado_asignaturasOD=[])
        print("incorporado LA sin asignaturas OD")
    db.session.add(nuevo_LA)
    db.session.commit()
    return make_response(jsonify({"Status" : "LA added"}))

# B.2) POST: INCORPORAR VARIOS LA
@app.route('/postendpoint/LAs', methods = ['POST'])
def add_LAs():
    request_data = request.get_json()
    #print(request_data)
    for i in range(0, len(request_data)):
        student_id = request_data[i]['id_estudiante']
        RRII_accept = request_data[i]["aceptado_RRII"]
        coord_accept = request_data[i]["aceptado_Coord"]
        RRII_sign = request_data[i]["fdo_RRII"]
        coord_sign = request_data[i]["fdo_Coord"]
        if "listado_asignaturasOD" in request_data[i]:
            #print("si hay listado asignaturas")
            asignaturas = request_data[i]["listado_asignaturasOD"]
            for i in range(0, len(asignaturas)):
                asignaturas_id = asignaturas[i]
                query_1 = db.session.query(Asignatura_Destino_Asignatura_Origen).filter(Asignatura_Destino_Asignatura_Origen.id == asignaturas_id)
                nuevo_LA = LA(id_estudiante=student_id, aceptado_RRII=RRII_accept, aceptado_Coord=coord_accept, fdo_RRII=RRII_sign, fdo_Coord=coord_sign, listado_asignaturasOD=query_1)
                print("incorporado LA CON asignaturas OD")
        else:
            nuevo_LA = LA(id_estudiante=student_id, aceptado_RRII=RRII_accept, aceptado_Coord=coord_accept, fdo_RRII=RRII_sign, fdo_Coord=coord_sign, listado_asignaturasOD=[])
            print("incorporado LA SIN asignaturas OD")
        db.session.add(nuevo_LA)
        db.session.commit()
    return make_response(jsonify({"Status" : "Varios LA Añadidos"}))

# C.3) DELETE: ELIMINAR TODOS LOS LA 
@app.route('/deleteAllLAs', methods=["DELETE"])
def erase_all_LAs():
    get_LAs = LA.query.all()
    #print("\n Los LA disponibles son: \n")
    #print(get_LAs)
    #print("\n")
    for i in get_LAs:
        #print("LAs que se va a eliminar: " + str(i))
        db.session.delete(i)
        db.session.commit()
    return make_response(jsonify({"Status" : "All LAs erased"}))



'''
ASIGNATURA_DESTINO_ASIGNATURA_ORIGEN
'''

# A) GET: MOSTRAR TODAS LAS AOD
@app.route('/aods', methods = ['GET'])
def Aods():
    get_aod_subjects = Asignatura_Destino_Asignatura_Origen.query.all()
    print(get_aod_subjects)
    AOD_schema = Asignatura_Destino_Asignatura_OrigenSchema(many=True)
    aod = AOD_schema.dump(get_aod_subjects)
    return make_response(jsonify({"Relacion(es) Asignaturas Origen y Destino": aod}))


# B.1) POST: INCORPORAR UN CONJUNTO DE ASIGNATURA DESTINO Y ORIGEN
@app.route('/postendpoint/Asignatura_destino_origen', methods = ['POST'])
def add_origin_and_destiny_subject():
    request_data = request.get_json()
    origin_subject_id = request_data["id_asignatura_origen"]
    destiny_subject_id = request_data["id_asignatura_destino"]
    nuevas_asignaturas = Asignatura_Destino_Asignatura_Origen(id_asignatura_destino=destiny_subject_id, id_asignatura_origen=origin_subject_id,)
    #print("nuevo AOD añadido \n")
    #print(nuevas_asignaturas)
    db.session.add(nuevas_asignaturas)
    db.session.commit()
    return make_response(jsonify({"Status" : "AOD added"}))



# B.2) POST: INCORPORAR VARIOS LA
@app.route('/postendpoint/various_Asignatura_destino_origen', methods = ['POST'])
def add_origin_and_destiny_subjects():
    request_data = request.get_json()
    for i in range(0, len(request_data)):
        origin_subject_id = request_data[i]["id_asignatura_origen"]
        destiny_subject_id = request_data[i]["id_asignatura_destino"]
        nuevas_asignaturas = Asignatura_Destino_Asignatura_Origen(id_asignatura_destino=destiny_subject_id, id_asignatura_origen=origin_subject_id,)
        #print("nuevo AOD añadido \n")
        #print(nuevas_asignaturas)
        db.session.add(nuevas_asignaturas)
        db.session.commit()
    return make_response(jsonify({"Status" : "Multiple AODs relations added"}))



# C.3) DELETE: ELIMINAR TODOS LAS AOD  
@app.route('/deleteAllAODs', methods=["DELETE"])
def erase_all_AODS():
    get_AODS = Asignatura_Destino_Asignatura_Origen.query.all()
    #print("\n Las Selecciones disponibles son: \n")
    #print(get_AODS)
    #print("\n")
    for i in get_AODS:
        #print("AODs que se van a eliminar: " + str(i))
        db.session.delete(i)
        db.session.commit()
    return make_response(jsonify({"Status" : "All AODS erased"}))




'''
SELECCION 
'''
# A) GET: MOSTRAR TODAS LAS SELECCIONES
@app.route('/Seleccion', methods = ['GET'])
def Selection():
    get_Seleccion = Seleccion.query.all()
    #print(get_Seleccion)
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
    if "estudiantes" in request_data:
        #print("si hay estudiante")
        list_1 = request_data["estudiantes"]
        for i in range(0, len(list_1)):
            student_id = list_1[i]
            query_1 = db.session.query(Estudiante).filter(Estudiante.id == student_id)
            nueva_seleccion = Seleccion(cuatri=term, año=year, vuelta=round, confirmacion=confirmation, estudiantes=query_1)
            print("seleccion incorporada CON estudiante")
    
    else:
        nueva_seleccion = Seleccion(cuatri=term, año=year, vuelta=round, confirmacion=confirmation, estudiantes=[])
        print("seleccion incorporada SIN estudiante")
    db.session.add(nueva_seleccion)
    db.session.commit()
    return make_response(jsonify({"Status" : "Selection added"}))


# (B.1_PRUEBA) POST: INCORPORAR UNA SELECCION FORMULARIO
@app.route('/seleccion_form', methods = ['GET','POST'])
def add_selection_form():
    if request.method == "POST":
        # getting input with name = fname in HTML form
       year = request.form.get("year")
       # getting input with name = lname in HTML form 
       term = request.form.get("duracion") 
       round = request.form.get("round") 
       confirmation = request.form.get("conf_uni") 
       try:
           students = request.form.get("estudiantes")
           # ARREGLAR ESTA PARTE DE AQUI
           nueva_seleccion = Seleccion(cuatri=term, año=year, vuelta=round, confirmacion=confirmation, estudiantes=students)
           print("seleccion incorporada sin estudiantes")

       except:
           nueva_seleccion = Seleccion(cuatri=term, año=year, vuelta=round, confirmacion=confirmation, estudiantes=[])
           print("seleccion incorporada con estudiantes")
       
       
       db.session.add(nueva_seleccion)
       db.session.commit()
       get_selecciones = Seleccion.query.all()
       seleccion_schema = SeleccionSchema(many=True)
       selecciones = seleccion_schema.dump(get_selecciones)
        # Estudiantes should have the object titles
       return make_response(jsonify({"Selecciones": selecciones}))

    return render_template("formulario_seleccion.html")
    
    

''' 
students_id = request_data["estudiantes"] #coge su id
    ### aqui iria el getter de estudiante en base a su id
    print(students_id)
    student = Estudiante.query.get(students_id)
    print(student) #este es el student
    print(type(student))
    print(student.nombre)
    nuevo_estudiante = Estudiante(nombre=student.nombre , apellidos=student.apellidos, curso=student.curso, grado=student.grado, titulo=student.titulo)
    nueva_seleccion = Seleccion(cuatri=term, año=year, vuelta=round, confirmacion=confirmation, estudiantes=nuevo_estudiante)
    #print("nueva seleccion añadida \n")
    #print(nueva_seleccion)

# B.1) POST: INCORPORAR UNA SELECCION
@app.route('/postendpoint/seleccion', methods = ['POST'])
def add_selection():
    request_data = request.get_json()
    term = request_data['cuatri']
    year = request_data["año"]
    round = request_data["vuelta"]
    confirmation = request_data["confirmacion"]
    students_id = request_data["estudiantes"] #coge su id
    ### aqui iria el getter de estudiante en base a su id
    print(students_id)
    student = Estudiante.query.get(students_id)
    print(student) #este es el student
    print(type(student))
    print(student.nombre)
    nuevo_estudiante = Estudiante(nombre=student.nombre , apellidos=student.apellidos, curso=student.curso, grado=student.grado, titulo=student.titulo)
    nueva_seleccion = Seleccion(cuatri=term, año=year, vuelta=round, confirmacion=confirmation, estudiantes=nuevo_estudiante)
    #print("nueva seleccion añadida \n")
    #print(nueva_seleccion)
    db.session.add(nueva_seleccion)
    db.session.commit()
    return make_response(jsonify({"Status" : "Selection added"}))
'''


# B.2) POST: INCORPORAR VARIAS SELECCIONES
@app.route('/postendpoint/selecciones', methods = ['POST'])
def add_selecciones():
    request_data = request.get_json()
    #print(request_data)
    for i in range(0, len(request_data)):
        term = request_data[i]['cuatri']
        year = request_data[i]["año"]
        round = request_data[i]["vuelta"]
        confirmation = request_data[i]["confirmacion"]
        #students = request_data[i]["estudiantes"]
        if "estudiantes" in request_data[i]:
            #print("si hay estudiante")
            list_1 = request_data[i]["estudiantes"]
            for i in range(0, len(list_1)):
                student_id = list_1[i]
                query_1 = db.session.query(Estudiante).filter(Estudiante.id == student_id)
                nueva_seleccion = Seleccion(cuatri=term, año=year, vuelta=round, confirmacion=confirmation, estudiantes=query_1)
                print("seleccion incorporada CON estudiante")
        else:
            nueva_seleccion = Seleccion(cuatri=term, año=year, vuelta=round, confirmacion=confirmation, estudiantes=[]) 
            print("seleccion incorporada SIN estudiante")
        #GETTER DE STUDENTS
        #print("nueva seleccion añadida \n")
        #print(nueva_seleccion)
        db.session.add(nueva_seleccion)
        db.session.commit()
    return make_response(jsonify({"Status" : "Varias Selecciones Añadidas"}))

# C.3) DELETE: ELIMINAR TODOS LAS SELECCIONES  
@app.route('/deleteAllSelecciones', methods=["DELETE"])
def erase_all_selections():
    get_selections = Seleccion.query.all()
    #print("\n Las Selecciones disponibles son: \n")
    #print(get_selections)
    #print("\n")
    for i in get_selections:
        #print("Selecciones que se van a eliminar: " + str(i))
        db.session.delete(i)
        db.session.commit()
    return make_response(jsonify({"Status" : "All Selections erased"}))















################### AUXILIARES EMPIEZAN AQUI #############################
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

# B.2) POST: INCORPORAR VARIAS SELECCIONES-UNIVERSIDADES
@app.route('/postendpoint/selecciones-universidades', methods = ['POST'])
def add_selections_universities():
    request_data = request.get_json()
    print(request_data)
    for i in range(0, len(request_data)):
        university_id = request_data[i]['id_universidad']
        selection_id = request_data[i]["id_seleccion"]
        nuevas_seleccion_universidad = Seleccion_Universidad(id_universidad=university_id, id_seleccion=selection_id) 
        print("nuevas selecciones-universidades añadida \n")
        print(nuevas_seleccion_universidad)
        db.session.add(nuevas_seleccion_universidad)
        db.session.commit()

    return make_response(jsonify({"Status" : "Varias Selecciones-Universidades Añadidas"}))

# C.3) DELETE: ELIMINAR TODOS LAS SELECCIONES  
@app.route('/deleteAllSelecciones_Universidades', methods=["DELETE"])
def erase_all_selections_universities():
    get_selections_universities = Seleccion_Universidad.query.all()
    print("\n Las Selecciones_Universidad disponibles son: \n")
    print(get_selections_universities)
    print("\n")
    for i in get_selections_universities:
        print("Selecciones_Universidades que se van a eliminar: " + str(i))
        db.session.delete(i)
        db.session.commit()
    
    return make_response(jsonify({"Status" : "All Selections_Universidades erased"}))


'''
SELECCION - ELECCION
'''

# A) GET: MOSTRAR TODAS LAS SELECCIONES-ESTUDIANTES
@app.route('/Seleccion-Estudiante', methods = ['GET'])
def Selection_Student():
    get_selection_student = auxiliar_estudiante_seleccion.query.all()
    selection_student_schema = auxiliar_estudiante_seleccion(many=True)
    selection_student = selection_student_schema.dump(get_selection_student)
    return make_response(jsonify({"Seleccion(es)-Universidad(es)": selection_student}))


# B.1) POST: INCORPORAR UNA SELECCION-ESTUDIANTE
@app.route('/postendpoint/seleccion-estudiante', methods = ['POST'])
def add_selection_student():
    request_data = request.get_json()
    student_id = request_data['id_estudiante']
    selection_id = request_data["id_seleccion"]
       
    nueva_seleccion_estudiante = auxiliar_estudiante_seleccion(id_estudiante=student_id, id_seleccion=selection_id)  
    print("nueva seleccion-estudiante añadida \n")
    print(nueva_seleccion_estudiante)
    db.session.add(nueva_seleccion_estudiante)
    db.session.commit()

    return make_response(jsonify({"Status" : "Selection-Student added"}))

# B.2) POST: INCORPORAR VARIAS SELECCIONES-ESTUDIANTES
@app.route('/postendpoint/selecciones-estudiantes', methods = ['POST'])
def add_selections_students():
    request_data = request.get_json()
    print(request_data)
    for i in range(0, len(request_data)):
        student_id = request_data[i]['id_estudiante']
        selection_id = request_data[i]["id_seleccion"]
        spots = request_data[i]["plaza"]
        accept = request_data[i]["aceptar"]
        nuevas_seleccion_estudiante = Estudiante_Seleccion(id_estudiante=student_id, id_seleccion=selection_id, plaza=spots, aceptar=accept) 
        print("nuevas selecciones-universidades añadida \n")
        print(nuevas_seleccion_estudiante)
        db.session.add(nuevas_seleccion_estudiante)
        db.session.commit()

    return make_response(jsonify({"Status" : "Varias Selecciones-Estudiantes Añadidas"}))

# C.3) DELETE: ELIMINAR TODOS LAS SELECCIONES-ESTUDIANTES  
@app.route('/deleteAllSelecciones_Estudiantes', methods=["DELETE"])
def erase_all_selections_students():
    get_selections_students = Estudiante_Seleccion.query.all()
    print("\n Las Selecciones_Estudiantes disponibles son: \n")
    print(get_selections_students)
    print("\n")
    for i in get_selections_students:
        print("Selecciones_Estudiantess que se van a eliminar: " + str(i))
        db.session.delete(i)
        db.session.commit()
    
    return make_response(jsonify({"Status" : "All Selections_Estudiantes erased"}))

''' from sqlalchemy import select, engine
# prueba acceso a tabla aux 
@app.route('/prueba/Seleccion-Estudiante', methods = ['GET'])
def prueba_Selection_Student():
    get_selection_student = select(auxiliar_estudiante_seleccion)
   
    result = fetchall(get_selection_student)
    #selection_student_schema = auxiliar_estudiante_seleccion(many=True)
    #selection_student = selection_student_schema.dump(get_selection_student)
    return make_response(jsonify({"Seleccion(es)-Universidad(es)": result}))
'''


    
'''
AOD - LA
'''

# A) GET: MOSTRAR TODAS LAS SELECCIONES-ESTUDIANTES
@app.route('/AOD_LAs', methods = ['GET'])
def get_AOD_LAs():
    get_AODS_LAs = AsignaturaOD_LA.query.all()
    AODs_LAs_Schema = AsignaturaOD_LASchema(many=True)
    selection_AODs_LAs = AODs_LAs_Schema.dump(get_AODS_LAs)
    return make_response(jsonify({"AOD(s) and LA(s)": selection_AODs_LAs}))


# B.1) POST: INCORPORAR UNA SELECCION-ESTUDIANTE
@app.route('/postendpoint/aod_La', methods = ['POST'])
def add_AOD_LA():
    request_data = request.get_json()
    AOD_id = request_data['id_AOD']
    LA_id = request_data["id_LA"]
    
    nueva_AOD_LA = AsignaturaOD_LA(id_AOD=AOD_id, id_LA=LA_id)  
    print(nueva_AOD_LA)
    db.session.add(nueva_AOD_LA)
    db.session.commit()

    return make_response(jsonify({"Status" : "Selection-Student added"}))

# B.2) POST: INCORPORAR VARIAS SELECCIONES-ESTUDIANTES
@app.route('/postendpoint/aods_Las', methods = ['POST'])
def add_AOD_LAs():
    request_data = request.get_json()
    print(request_data)
    for i in range(0, len(request_data)):
        AOD_id = request_data[i]['id_AOD']
        LA_id = request_data[i]["id_LA"]
        
        nueva_AOD_LA = AsignaturaOD_LA(id_AOD=AOD_id, id_LA=LA_id)  
        print(nueva_AOD_LA)
        db.session.add(nueva_AOD_LA)
        db.session.commit()
        db.session.commit()

    return make_response(jsonify({"Status" : "Varias AOD-LA Añadidas"}))


# C.3) DELETE: ELIMINAR TODOS LAS SELECCIONES-ESTUDIANTES  
@app.route('/deleteAllAODsLAs', methods=["DELETE"])
def erase_all_AOD_LAs():
    get_AODS_LAs = AsignaturaOD_LA.query.all()
    print("\n Las AOD - LA disponibles son: \n")
    print(get_AODS_LAs)
    print("\n")
    for i in get_AODS_LAs:
        print("AOD - LA  que se van a eliminar: " + str(i))
        db.session.delete(i)
        db.session.commit()
    
    return make_response(jsonify({"Status" : "All AOD-LA erased"}))






#################### PRUEBAS


# prueba de insert en una tabla aux seleccion - estudiantes
@app.route('/postendpoint/prueba_seleccion_estudiante', methods = ['POST'])
def prueba_add_selections_students():
    request_data = request.get_json()
    #print(request_data)
    for i in range(0, len(request_data)):
        student_id = request_data[i]['id_estudiante']
        selection_id = request_data[i]["id_seleccion"]
        db.session.execute(auxiliar_estudiante_seleccion.insert().values(id_estudiante=student_id, id_seleccion=selection_id))
        #print("nuevas selecciones-estudiantes añadida \n")
        db.session.commit()
    return make_response(jsonify({"Status" : "Varias Selecciones-Estudiantes Añadidas"}))




# prueba de insert en una tabla seleccion - universidad
@app.route('/postendpoint/prueba_seleccion_universidad', methods = ['POST'])
def prueba_add_selections_universities():
    request_data = request.get_json()
    #print(request_data)
    for i in range(0, len(request_data)):
        university_id = request_data[i]['id_universidad']
        selection_id = request_data[i]["id_seleccion"]
        order = request_data[i]["orden"]
        accept = request_data[i]["aceptar"]
        db.session.execute(auxiliar_universidad_seleccion.insert().values(id_universidad=university_id, id_seleccion=selection_id, aceptar=accept, orden=order))
        #print("nuevas selecciones-universidades añadida \n")
        db.session.commit()
    return make_response(jsonify({"Status" : "Varias Selecciones-Universidades Añadidas"}))


# prueba de insert en una tabla la - ASIGNATURA_DES_OR
@app.route('/postendpoint/prueba_la_asignaturas', methods = ['POST'])
def prueba_add_subjects_las():
    request_data = request.get_json()
    #print(request_data)
    for i in range(0, len(request_data)):
        la_id = request_data[i]['id_LA']
        subjects_id = request_data[i]["id_AOD"]
        db.session.execute(auxiliar_LA_asignaturasOD.insert().values(id_LA=la_id, id_AOD=subjects_id))
        #print("nuevas las-AODs añadida \n")
        db.session.commit()

    return make_response(jsonify({"Status" : "Varias LAs-AODs Añadidas"}))



#prueba de un caso de uso - estudiantes de un proceso de seleccion
@app.route('/seleccion/<yy>/<term>', methods = ['GET'])
def get_students_selecctionprocess(year, term):
    year = Seleccion.query.get("año")
    term = Seleccion.query.get("cuatri")
    
    db.session.commit()
    return redirect('/estudiantes')
