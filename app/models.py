from flask import Flask, redirect, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import true
from . import app, db


class Estudiante(db.Model):
    '''
    Clase: Student

    Atributos:
        ID: Int, clave primaria
        Nombre: Str(30)
        Apellidos: Str(50)
        Curso: Int (1-6)
        Grado: Str(30) - Enum de grados?
        Titulo: ---- no se como poner esto porque podría ser una lista o diccionario que tenga varios idiomas y un si o no y nivel ---

    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "Estudiantes"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))
    apellidos = db.Column(db.String(50))
    curso = db.Column(db.Integer)
    grado = db.Column(db.String(30))
    titulo = db.Column(db.String(30))

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,nombre,apellidos,curso,grado,titulo):
        self.nombre = nombre
        self.apellidos = apellidos
        self.curso = curso
        self.grado = grado
        self.titulo = titulo

    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.apellidos}:{self.id}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Nombre":self.nombre, "Apellidos":self.apellidos, "Curso":self.curso, "Grado":self.grado, "Titulo":self.titulo}

# 2º
# Despues generate masrshmallow schemas from your model using SQLAlchemyAutoSchema
class EstudianteSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Estudiante
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        nombre = fields.String(required=True)
        apellidos = fields.String(required=True)
        curso = fields.Int(required=True)
        grado = fields.String(required=True)
        titulo = fields.String(required=True)


class Seleccion(db.Model):
    '''
    Clase: Seleccion

    Atributos:
        ID_universidad: Int
        ID_estudiante: Int
        plazas: Str(30)
        confirmaciones: Str(50)
        cuatri: Int (1-2)
        año: Int() ---- podria ponerse formato datetime
        vuelta: Int (1-2)

    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "Seleccion"
    id_universidad = db.Column(db.Integer)
    id_estudiante = db.Column(db.Integer)
    plazas = db.Column(db.String(30))
    confirmaciones = db.Column(db.String(50))
    cuatri = db.Column(db.Integer)
    año = db.Column(db.Integer)
    vuelta = db.Column(db.Integer)

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,id_universidad, id_estudiante, plazas, confirmaciones, cuatri, año, vuelta):
        self.id_universidad = id_universidad
        self.id_estudiante = id_estudiante
        self.plazas = plazas
        self.confirmaciones = confirmaciones
        self.cuatri = cuatri
        self.año = año
        self.vuelta = vuelta

    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        #return f"{self.id_estudiante}:{self.id}"
    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"ID Universidad Destino":self.id_universidad, "ID Estudiante":self.id_estudiante, "Año":self.año, "Cuatrimestre":self.cuatri, "Vuelta":self.vuelta, "Confirmaciones":self.confirmaciones, "Plazas":self.plazas}

class Universidad(db.Model):
    '''
    Clase: Universidad

    Atributos:
        ID: Int, clave primaria
        Nombre: Str(30) Nombre de la universidad de destino
        Ubicación: Str(50) País y ciudad?
        
    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "Universidad"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))
    ubicacion = db.Column(db.String(50))

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,nombre,ubicacion):
        self.nombre = nombre
        self.ubicacion = ubicacion

    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        #return f"{self.apellidos}:{self.id}"
    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Nombre":self.nombre, "Ubicación":self.ubicacion}

class Asignatura_Origen(db.Model):
    '''
    Clase: ASignatura Origen

    Atributos:
        ID: Int, clave primaria
        
    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "Asignatura_Origen"
    id = db.Column(db.Integer, primary_key=True)

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    #def __init__(self,nombre,apellidos,curso,grado,titulo):
    
    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        #return f"{self.apellidos}:{self.id}"

    #def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Nombre":self.nombre, "Apellidos":self.apellidos, "Curso":self.curso, "Grado":self.grado, "Titulo":self.titulo}

class Asignatura_Destino(db.Model):
    '''
    Clase: Asignatura_Destino

    Atributos:
        ID: Int, clave primaria
        Universidad: Str(30) universidad en la que se imparte
        ID_universidad: Int
        
    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "Asignatura_Destino"
    id = db.Column(db.Integer, primary_key=True)
    universidad = db.Column(db.String(30))
    id_universidad = (db.Integer)
    

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,universidad,id_universidad):
        self.universidad = universidad
        self.id_universidad = id_universidad
   

    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.universidad}:{self.id}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Universidad Destino":self.universidad, "ID Universidad":self.id_universidad}

class LA(db.Model):
    '''
    Clase: Learning Agreement

    Atributos:
        ID: Int, clave primaria
        ID_estudiante: Int
        ID_asignatura_destino: Int
        ID_asignatura_origen: Int
        aceptado_RRII: bool
        aceptado_Coord: bool
        fdo_RRII: bool
        fdo_Coord: bool

    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "LA"
    id = db.Column(db.Integer, primary_key=True)
    id_estudiante = db.Column(db.Integer)
    id_asignatura_d = db.Column(db.Integer)
    id_asignatura_o = db.Column(db.Integer)
    aceptado_RRII = db.Column(db.Bool)
    aceptado_Coord = db.Column(db.Bool)
    fdo_RRII = db.Column(db.Bool)
    fdo_RRII = db.Column(db.Bool)

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,id_estudiante,id_asignatura_d,id_asignatura_o,aceptado_RRII,aceptado_Coord, fdo_RRII, fdo_Coord):
        self.id_estudiante = id_estudiante  
        self.id_asignatura_d = id_asignatura_d
        self.id_asignatura_o = id_asignatura_o
        self.aceptado_RRII = aceptado_RRII
        self.aceptado_Coord = aceptado_Coord
        self.fdo_RRII = fdo_RRII
        self.fdo_Coord = fdo_Coord

    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        #return f"{self.apellidos}:{self.id}"
    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"ID_Estudiante":self.id_estudiante, "ID_Asignatura_Origen":self.id_asignatura_o, "ID_Asignatura_Destino":self.id_asignatura_d, "Aceptado RRII":self.aceptado_RRII,  "Aceptado Coord":self.aceptado_Coord, "Firmado RRII":self.fdo_RRII, "Firmado Coord":self.fdo_Coord,}

db.create_all()