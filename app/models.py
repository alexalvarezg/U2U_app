from flask import Flask, redirect, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import true
from . import app, db

# 1º
# Declaras el modelo como normal
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


db.create_all()