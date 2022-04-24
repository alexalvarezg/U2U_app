from tkinter import E
from . import app, db
from .models import *
from flask import redirect, jsonify, make_response, render_template, request
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