from tkinter import E
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