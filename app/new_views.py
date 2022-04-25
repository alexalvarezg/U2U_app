from tkinter import E

from zmq import EVENT_CLOSE_FAILED
from . import app, db
from .models import *
from flask import redirect, jsonify, make_response, render_template, request, request_finished
from flask import render_template
from sqlalchemy import text

#para el login y registration
from flask import Flask,render_template,request,redirect,session,flash,url_for
from functools import wraps



@app.route("/")
def welcome():
   return "This is a flask app"


@app.route('/login',methods=['POST','GET'])
def login():
    status=True
    if request.method=='POST':
        email=request.form["email"]
        pwd=request.form["password"]
        data = db.engine.execute("select * from users where email=%s and password=%s",(email,pwd)).fetchone()
        if data:
            session['logged_in']=True
            session['username']=data["nombre"]
            flash('Login Successfully','success')
            return redirect('/main')
        else:
            flash('Email o contraseña incorrectos. Por favor, pruebe de nuevo','danger')
    return render_template("login.html")
#check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized, Please Login','danger')
			return redirect(url_for('login'))
	return wrap









# --------------------------------------------------------------------------------------------------------------------------- TITULO IDIOMA

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
    type = request_data['tipo']
    score = request_data['puntuacion']
    
    nuevo_titulo = Titulo(idioma=language , nivel=level, tipo=type, puntuacion=score) 
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
        type = request_data[i]['tipo']
        score = request_data[i]['puntuacion']
        nuevo_titulo = Titulo(idioma=language , nivel=level, tipo=type, puntuacion=score) 
        #print(nuevo_estudiante)
        db.session.add(nuevo_titulo)
        db.session.commit()
    return make_response(jsonify({"Status" : "Various Titulos added"}))


# --------------------------------------------------------------------------------------------------------------------------- TITULACIONES
# A) GET: MOSTRAR TODOS LAS TITULACIONES
@app.route('/titulaciones', methods = ['GET'])
def see_titulaciones():
    get_titulaciones = Titulacion.query.all()
    titulacion_schema = TitulacionSchema(many=True)
    titulaciones = titulacion_schema.dump(get_titulaciones)
    return make_response(jsonify({"Titulaciones": titulaciones}))


# B.1) POST: INCORPORAR UN TITULO
@app.route('/postendpoint/titulacion', methods = ['POST'])
def add_titulacion():
    request_data = request.get_json()
    name = request_data['nombre']
    code = request_data['codigo']
    
    nueva_titulacion = Titulacion(nombre=name, codigo=code)  
    #print(nuevo_titulo)
    db.session.add(nueva_titulacion)
    db.session.commit()
    return make_response(jsonify({"Status" : "Titulacion added"}))

# B.2) POST: INCORPORAR VARIOS TITULOS
@app.route('/postendpoint/titulaciones', methods = ['POST'])
def add_titulaciones():
    request_data = request.get_json()
    #print(request_data)
    for i in range(0, len(request_data)):
        name = request_data[i]['nombre']
        code = request_data[i]['codigo']
    
        nueva_titulacion = Titulacion(nombre=name, codigo=code)
        #print(nuevo_estudiante)
        db.session.add(nueva_titulacion)
        db.session.commit()
    return make_response(jsonify({"Status" : "Various Titulaciones added"}))




# --------------------------------------------------------------------------------------------------------------------------- UNIVERSIDAD
# A) GET: MOSTRAR TODOS LAS UNIVERSIDADES
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
    spots1 = request_data["plazas1"]
    spots2 = request_data["plazas2"]
    if "titulo" in request_data:
        title = request_data["titulo"][0]
        query_1 = db.session.query(Titulo).filter(Titulo.id == title)
        if "titulaciones" in request_data:
            degree = request_data["titulaciones"][0]
            query_2 = db.session.query(Titulacion).filter(Titulacion.id == degree)
            nueva_universidad = Universidad(nombre=name, ubicacion=place, plazas1=spots1, plazas2=spots2, titulo=query_1, titulaciones=query_2)
        else:
            nueva_universidad = Universidad(nombre=name, ubicacion=place, plaza_1=spots1, plazas2=spots2, titulo=query_1, titulaciones=[])
    else:
        if "titulaciones" in request_data:
            degree = request_data["titulaciones"][0]
            query_2 = db.session.query(Titulacion).filter(Titulacion.id == degree)
            nueva_universidad = Universidad(nombre=name, ubicacion=place, plazas1=spots1, plazas2=spots2, titulo=[], titulaciones=query_2) 
        else: 
            nueva_universidad = Universidad(nombre=name, ubicacion=place, plazas1=spots1, plazas2=spots2, titulo=[], titulaciones=[]) 
    db.session.add(nueva_universidad)
    db.session.commit()
    return make_response(jsonify({"Status" : "Universidad added"}))


# B.2) POST: INCORPORAR VARIAS UNIVERSIDADES
@app.route('/postendpoint/universidades', methods = ['POST'])
def add_universities():
    request_data = request.get_json()
    for i in range(0, len(request_data)):
        name = request_data[i]['nombre']
        place = request_data[i]["ubicacion"]
        spots1 = request_data[i]["plazas1"]
        spots2 = request_data[i]["plazas2"]
        if "titulo" in request_data[i]:
            title = request_data[i]["titulo"]
            query_1 = db.session.query(Titulo).filter(Titulo.id == title)
            if "titulaciones" in request_data[i]:
                degree = request_data[i]["titulaciones"]
                query_2 = db.session.query(Titulacion).filter(Titulacion.id == degree)
                nueva_universidad = Universidad(nombre=name, ubicacion=place, plazas1=spots1, plazas2=spots2, titulo=query_1, titulaciones=query_2)
            else:
                nueva_universidad = Universidad(nombre=name, ubicacion=place, plaza_1=spots1, plazas2=spots2, titulo=query_1, titulaciones=[])
        else:
            if "titulaciones" in request_data[i]:
                degree = request_data[i]["titulaciones"]
                query_2 = db.session.query(Titulacion).filter(Titulacion.id == degree)
                nueva_universidad = Universidad(nombre=name, ubicacion=place, plazas1=spots1, plazas2=spots2, titulo=[], titulaciones=query_2) 
            else: 
                nueva_universidad = Universidad(nombre=name, ubicacion=place, plazas1=spots1, plazas2=spots2, titulo=[], titulaciones=[]) 
        db.session.add(nueva_universidad)
        db.session.commit()
    return make_response(jsonify({"Status" : "Varias Universidades Añadidas"}))



# --------------------------------------------------------------------------------------------------------------------------- REQUSIITOS
# A) GET: MOSTRAR TODOS LOS REQUISITOS
@app.route('/requisitos', methods = ['GET'])
def requisitos():
    get_requisitos = Requisitos.query.all()
    Requisitos_schema = RequisitosSchema(many=True)
    requisitos = Requisitos_schema.dump(get_requisitos)
    return make_response(jsonify({"Requisitos": requisitos}))

# B.1) POST: INCORPORAR UN TITULO
@app.route('/postendpoint/requisitos', methods = ['POST'])
def add_requisito():
    request_data = request.get_json()
    name = request_data['nombre']
    
    nuevo_requisito = Requisitos(nombre=name)  
    db.session.add(nuevo_requisito)
    db.session.commit()
    return make_response(jsonify({"Status" : "Requisito added"}))


# B.2) POST: INCORPORAR VARIOS REQUISITOS
@app.route('/postendpoint/requisitos', methods = ['POST'])
def add_requisitos():
    request_data = request.get_json()
    #print(request_data)
    for i in range(0, len(request_data)):
        name = request_data[i]['nombre']
    
        nuevo_requisito = Requisitos(nombre=name)  
        db.session.add(nuevo_requisito)
        db.session.commit()
    return make_response(jsonify({"Status" : "Various Requisitos added"}))




# --------------------------------------------------------------------------------------------------------------------------- ESTUDIANTES
# A) GET: MOSTRAR TODOS LOS ESTUDIANTES
@app.route('/estudiantes', methods = ['GET'])
def students():
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
    #title = request_data["titulo"]
    print("**************************")
    if "titulo" in request_data:
        titles = request_data["titulo"]
        query_1 = db.session.query(Titulo).filter(Titulo.id == titles)
    else:
        query_1 = []


    if "id_requisito" in request_data:
        requisite = request_data["id_requisito"]
        query_2 = db.session.query(Requisitos).filter(Requisitos.id == requisite)
    else:
        query_2 = []


    if  "pre_seleccion" in request_data:
        pre_selection = request_data["pre_seleccion"]
    else: 
        pre_selection = []
    
    if "seleccion"  in request_data:
        selection = request_data["seleccion"]
    else:
        selection = []

    nuevo_estudiante = Estudiante(nombre=name , apellidos=surname, curso=grade, grado=degree, titulo=query_1, id_requisito=query_2, pre_seleccion=pre_selection, seleccion=selection)

    #print(nuevo_estudiante)
    db.session.add(nuevo_estudiante)
    db.session.commit()
    return make_response(jsonify({"Status" : "Sudent added"}))



# (B.1_PRUEBA) POST: INCORPORAR UN ESTUDIANTE FORMULARIO --------------------------------------------------------------------------------------------------------------------------- MODIFICAR
@app.route('/nuevo_estudiante', methods = ['GET','POST'])
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

    return render_template("Admin/Nuevo_Estudiante.html")



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
            title = request_data[i]['titulo'][0]
            query_1 = db.session.query(Titulo).filter(Titulo.id == title)
        else:
            query_1 = []


        if "id_requisito" in request_data[i]:
            requisite = request_data[i]["id_requisito"]
            query_2 = db.session.query(Requisitos).filter(Requisitos.id == requisite)
        else:
            query_2 = []


        if  "pre_seleccion" in request_data[i]:
            pre_selection = request_data[i]["pre_seleccion"]
        else: 
            pre_selection = []
        
        if "seleccion" in request_data[i]:
            selection = request_data[i]["seleccion"]
        else:
            selection = []

        nuevo_estudiante = Estudiante(nombre=name , apellidos=surname, curso=grade, grado=degree, titulo=query_1, id_requisito=query_2, pre_seleccion=pre_selection, seleccion=selection)
        print("nuevo estudiante incorporado")

        db.session.add(nuevo_estudiante)
        db.session.commit()
    return make_response(jsonify({"Status" : "Various Students added"}))




# --------------------------------------------------------------------------------------------------------------------------- ASIGNATURAS DE ORIGEN
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
    code = request_data['codigo']
    grade = request_data['curso']
    degree = request_data['titulaciones']
    nueva_asignatura = Asignatura_Origen(nombre=name, codigo=code, curso=grade, titulaciones=degree)
    db.session.add(nueva_asignatura)
    db.session.commit()
    return make_response(jsonify({"Status" : "Asignatura de origen added"}))


# B.2) POST: INCORPORAR VARIAS ASIGNATURAS DE ORIGEN
@app.route('/postendpoint/asignaturas_origen', methods = ['POST'])
def add_subjects():
    request_data = request.get_json()
    for i in range(0, len(request_data)):
        name = request_data[i]['nombre']
        code = request_data[i]['codigo']
        grade = request_data[i]['curso']
        if "titulaciones" in request_data[i]:
            degree = request_data[0]['titulaciones']
        else:
            degree = []

        nueva_asignatura = Asignatura_Origen(nombre=name, codigo=code, curso=grade, titulaciones=degree)
        db.session.add(nueva_asignatura)
        db.session.commit()
    return make_response(jsonify({"Status" : "Various Subjects added"}))



# --------------------------------------------------------------------------------------------------------------------------- ASIGNATURAS DE DESTINO
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
    code = request_data['codigo']
    university_id = request_data['id_universidad']
    nueva_asignatura = Asignatura_Destino(nombre=name, codigo=code,  id_universidad=university_id)
    db.session.add(nueva_asignatura)
    db.session.commit()
    return make_response(jsonify({"Status" : "Asignatura de destino added"}))



# B.2) POST: INCORPORAR VARIAS ASIGNATURAS DE DESTINO
@app.route('/postendpoint/asignaturas_destino', methods = ['POST'])
def add_subjects_abroad():
    request_data = request.get_json()
    for i in range(0, len(request_data)):
        name = request_data[i]['nombre']
        code = request_data[i]['codigo']
        university_id = request_data[i]['id_universidad']
        nueva_asignatura = Asignatura_Destino(nombre=name, codigo=code, id_universidad=university_id)
        db.session.add(nueva_asignatura)
        db.session.commit()
    return make_response(jsonify({"Status" : "Various Subjects added"}))



# --------------------------------------------------------------------------------------------------------------------------- ASIGNATURAS DE DESTINO - ORIGEN
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


# B.2) POST: INCORPORAR VARIOS CONJUNTOS DE ASIGNATURA DESTINO Y ORIGEN
@app.route('/postendpoint/various_Asignatura_destino_origen', methods = ['POST'])
def add_origin_and_destiny_subjects():
    request_data = request.get_json()
    for i in range(0, len(request_data)):
        origin_subject_id = request_data[i]["id_asignatura_origen"]
        destiny_subject_id = request_data[i]["id_asignatura_destino"]
        nuevas_asignaturas = Asignatura_Destino_Asignatura_Origen(id_asignatura_destino=destiny_subject_id, id_asignatura_origen=origin_subject_id,)
        db.session.add(nuevas_asignaturas)
        db.session.commit()
    return make_response(jsonify({"Status" : "Multiple AODs relations added"}))



# --------------------------------------------------------------------------------------------------------------------------- LEARNING AGREEMENT
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
    print("incorporado LA")
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
        nuevo_LA = LA(id_estudiante=student_id, aceptado_RRII=RRII_accept, aceptado_Coord=coord_accept, fdo_RRII=RRII_sign, fdo_Coord=coord_sign)
        print("incorporado LA SIN asignaturas OD")
        db.session.add(nuevo_LA)
        db.session.commit()
    return make_response(jsonify({"Status" : "Varios LA Añadidos"}))


# --------------------------------------------------------------------------------------------------------------------------- ASOCIACIONLA_A
# A) GET: MOSTRAR TODOS LOS ASOCIACIONLA_A 
@app.route('/asociacionLA_A', methods = ['GET'])
def AsociacionLA_a():
    get_AsociacionLA_a = AsociacionLA_A.query.all()
    AsociacionLA_A_schema = AsociacionLA_ASchema(many=True)
    Asociaciones = AsociacionLA_A_schema.dump(get_AsociacionLA_a)
    return make_response(jsonify({"AsociacionesLA_A": Asociaciones}))


# B.1) POST: INCORPORAR UN REGISTRO DE ASOCIACIONLA_A
@app.route('/postendpoint/asociacionLA_A', methods = ['POST'])
def add_AsociacionLA_a():
    request_data = request.get_json()
    cancellation = request_data['cancelado']
    cancellation_date = request_data["fecha_cancelacion"]
    reason = request_data["motivo"]
    accepted = request_data["aceptado"]
    accepted_date = request_data["fecha_aceptacion"]
    la_id = request_data['id_LA']
    subjects_id = request_data['id_asignatura_OD']

    nuevo_AsociacionLA_a = AsociacionLA_A(cancelado=cancellation, fecha_cancelacion=cancellation_date, motivo=reason, aceptado=accepted, fecha_aceptacion=accepted_date, id_LA=la_id, id_asignatura_OD=subjects_id)
    print("incorporado AsociacionLA_A")
    db.session.add(nuevo_AsociacionLA_a)
    db.session.commit()
    return make_response(jsonify({"Status" : "ASociacionLA_A added"}))

'''
{
    "cancelado": 0, 
    "fecha_cancelacion": "", 
    "motivo": "no se ha cancelado aun", 
    "aceptado":1, 
    "fecha_aceptacion":"", 
    "id_LA": 2,
    "id_asignatura_OD": 2
}
'''

# B.2) POST: INCORPORAR VARIOS LA
@app.route('/postendpoint/asociacionesLA_a', methods = ['POST'])
def add_AsociacionLA_as():
    request_data = request.get_json()
    #print(request_data)
    for i in range(0, len(request_data)):
        cancellation = request_data[i]['cancelado']
        cancellation_date = request_data[i]["fecha_cancelacion"]
        reason = request_data[i]["motivo"]
        accepted = request_data[i]["aceptado"]
        accepted_date = request_data[i]["fecha_aceptacion"]
        la_id = request_data[i]['id_LA']
        subjects_id = request_data[i]['id_asignatura_OD']
        nuevo_AsociacionLA_a = AsociacionLA_A(cancelado=cancellation, fecha_cancelacion=cancellation_date, motivo=reason, aceptado=accepted, fecha_aceptacion=accepted_date, id_LA=la_id, id_asignatura_OD=subjects_id)
        print("incorporado AsociacionLA_A")
        db.session.add(nuevo_AsociacionLA_a)
        db.session.commit()
    return make_response(jsonify({"Status" : "Varios ASociacionLA_A Añadidos"}))



# --------------------------------------------------------------------------------------------------------------------------- ASOCIACIONLA_A
# A) GET: MOSTRAR TODOS LOS ENLACESAD
@app.route('/enlaceAD', methods = ['GET'])
def enlaceAD():
    get_enlaces = EnlaceAD.query.all()
    EnlaceAD_Schema = EnlaceADSchema(many=True)
    Enlaces = EnlaceAD_Schema.dump(get_enlaces)
    return make_response(jsonify({"Enlaces": Enlaces}))


# B.1) POST: INCORPORAR UN REGISTRO DE ENLACEAD
@app.route('/postendpoint/enlaceAD', methods = ['POST'])
def add_enlaceAD():
    request_data = request.get_json()
    year = request_data['año']
    web_link = request_data["link"]
    term = request_data["cuatri"]
    subject_id = request_data["id_asignatura_destino"]
   
    nuevo_EnlaceAD = EnlaceAD(año=year, link=web_link, cuatri=term, id_asignatura_destino=subject_id)
    print("incorporado nuevo_EnlaceAD")
    db.session.add(nuevo_EnlaceAD)
    db.session.commit()
    return make_response(jsonify({"Status" : "nuevo_EnlaceAD added"}))



# B.1) POST: INCORPORAR VARIOS REGISTRO DE ENLACEAD
@app.route('/postendpoint/enlacesAD', methods = ['POST'])
def add_enlacesAD():
    request_data = request.get_json()
    for i in range(0, len(request_data)):
        request_data = request.get_json()
        year = request_data[i]['año']
        web_link = request_data[i]["link"]
        term = request_data[i]["cuatri"]
        subject_id = request_data[i]["id_asignatura_destino"]
    
        nuevo_EnlaceAD = EnlaceAD(año=year, link=web_link, cuatri=term, id_asignatura_destino=subject_id)
        print("incorporado nuevo_EnlaceAD")
        db.session.add(nuevo_EnlaceAD)
        db.session.commit()
    return make_response(jsonify({"Status" : "Nuevos EnlaceAD added"}))

