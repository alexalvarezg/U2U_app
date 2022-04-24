from __future__ import unicode_literals
from ast import Index, dump
from tkinter.tix import Tree
from unicodedata import name
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from . import db

from sqlalchemy import UniqueConstraint

from sqlalchemy import insert
#from app import db



#Base = declarative_base()




'''
TABLAS AUXILIARES RELACIONES (N,M)
'''

## ESTUDIANTE - TITULO IDIOMA
auxiliar_Titulo_Estudiantes = db.Table('aux_titulo_estudiante', 
    db.Column('id_estudiante', db.Integer, db.ForeignKey('Estudiantes.id'), primary_key=True), 
    db.Column('id_titulo', db.Integer, db.ForeignKey('Titulo.id'), primary_key = True)
)

## UNIVERSIDAD DE DESTINO - TITULO IDIOMA
auxiliar_Titulo_Universidad = db.Table('aux_titulo_universidad', 
    db.Column('id_universidad', db.Integer, db.ForeignKey('Universidad.id'), primary_key=True), 
    db.Column('id_titulo', db.Integer, db.ForeignKey('Titulo.id'), primary_key = True)
)

## (PRE SELECCION) ESTUDIANTE - UNIVERSIDAD DE DESTINO
auxiliar_pre_seleccion = db.Table('aux_pre_seleccion', 
    db.Column('id_universidad', db.Integer, db.ForeignKey('Universidad.id'), primary_key=True), 
    db.Column('id_estudiante', db.Integer, db.ForeignKey('Estudiantes.id'), primary_key=True), 
    db.Column('año', db.Integer, nullable=False), 
    db.Column('cuatri', db.Integer, nullable=False), 
    db.Column('orden', db.Integer, nullable=False) # esto no puede ser un integer, deberia ser una lista o algo
)

## (SELECCION) ESTUDIANTE - UNIVERSIDAD DESTINO
auxiliar_seleccion = db.Table('aux_seleccion', 
    db.Column('id_universidad', db.Integer, db.ForeignKey('Universidad.id'), primary_key=True), 
    db.Column('id_estudiante', db.Integer, db.ForeignKey('Estudiantes.id'), primary_key=True), 
    db.Column('año', db.Integer, nullable=False), 
    db.Column('cuatri', db.Integer, nullable=False), 
    db.Column('vuelta', db.Integer, nullable=False)
)

## TITULACIONES - UNIVERSIDAD DE DESTINO



## ASIGNATURAS ORIGEN - TITULACIONES











'''
ENTIDADES - SEGURIDAD
'''
# ------------------------------------------------------------------------ USUARIO
class User(db.Model):
    '''
    Clase: Usuario

    Atributos:
        ID: Int, clave primaria
        nombre: 
        email: 
        password

    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "Users"
    __table_args__ = (
        db.UniqueConstraint('email'),
    )

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)


    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,nombre, email, password):
        self.nombre = nombre
        self.email = email
        self.password = password
    

    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.name}:{self.email}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"nombre":self.nombre, "amail":self.email, "password": self.password}

class User_Schema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = User
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        nombre = fields.String(required=True)
        email = fields.String(required=True)
        password = fields.String(required=True)






'''
ENTIDADES DIAGRAMA ENTIDAD RELACION 
'''

# ------------------------------------------------------------------------ TITULO IDIOMA
class Titulo(db.Model):
    '''
    Clase: Titulo de idioma

    Atributos:
        ID: Int, clave primaria
        idioma: 
        nivel: 
        tipo: 
        puntuacion: podemos permitir que la puntuacion sea un 0 si el titulo no lleva asociada puntuacion
        
    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "Titulo"
    __table_args__ = (
        db.UniqueConstraint('idioma', 'nivel', 'tipo', name='unique_titulo:idioma'),
    )
    id = db.Column(db.Integer, primary_key=True)
    idioma = db.Column(db.String(255), nullable=False)
    nivel = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(255), nullable=False)
    puntuacion = db.Column(db.Integer, nullable=True) #deberiamos hacer que una vez los titulos fueran insertados, una funcion recorriese la tabla tituulos y modificase cada linea incorporadno la puntuacion correspondiente


    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,idioma, nivel, tipo, puntuacion):
        self.idioma = idioma
        self.nivel = nivel
        self.tipo = tipo
        self.puntuacion = puntuacion
    
    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.tipo}:{self.nivel}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Idioma":self.idioma, "nivel":self.nivel, "tipo":self.tipo, "puntuacion":self.puntuacion}

class Titulo_Schema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Titulo
        include_relationships = True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        idioma = fields.String(required=True)
        nivel = fields.String(required=True)
        tipo = fields.String(required=True)
        puntuacion = fields.Integer(required=False)



# ------------------------------------------------------------------------ UNIVERSIDAD DE DESTINO
class Universidad(db.Model):
    '''
    Clase: Universidad

    Atributos:
        ID: Int, clave primaria
        Nombre: Str(30) Nombre de la universidad de destino
        Ubicación: Str(50) País y ciudad
        plazas1: numero de plazas disponibles en la universidad de destino para el primer cuatrimestre
        plazas2: numero de plazas disponibles en la universidad de destino para el segundo cuatrimestre

    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "Universidad"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    ubicacion = db.Column(db.String(50), nullable=False)
    plazas_1 = db.Column(db.Integer, nullable=True) 
    plazas_2 = db.Column(db.Integer, nullable=True) 
    # asociado a la tabla auxiliar TITULO - UNIVERSIDAD
    titulo = db.relationship("Titulo", secondary=auxiliar_Titulo_Universidad, backref=backref('Universidad', lazy='dynamic'), lazy='dynamic')
    
    
    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,nombre,ubicacion, plazas1, plazas2,titulo):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.plazas1 = plazas1
        self.plazas2 = plazas2
        self.titulo = titulo

    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.nombre}:{self.id}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Nombre":self.nombre, "Ubicación":self.ubicacion, "Plazas primer cuatri":self.plazas1, "Plazas segundo cuatri":self.plazas2,"Titulo": self.titulo}

class UniversidadSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Universidad
        include_relationships = True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        nombre = fields.String(required=True)
        ubicacion = fields.String(required=True)
        plazas1 = fields.Integer(required=True)
        plazas2 = fields.Integer(required=True)
        titulo = fields.List



# ------------------------------------------------------------------------ TITULACIONES UNIVERSITARIAS
class Titulacion(db.Model):
    '''
    Clase: Titulacion

    Atributos:
        ID: Int, clave primaria
        nombre: Str(30) Nombre de la universidad de destino
        codigo: abreviatura de la titulacion

    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "Titulaciones"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    codigo = db.Column(db.String(30), nullable=False)
    
    
    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,nombre,codigo):
        self.nombre = nombre
        self.codigo = codigo
        
    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.nombre}:{self.codigo}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Nombre":self.nombre, "Codigo": self.codigo}

class TitulacionSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Titulacion
        include_relationships = True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        nombre = fields.String(required=True)
        codigo = fields.String(required=True)




# ------------------------------------------------------------------------ REQUISITOS



# ------------------------------------------------------------------------ ESTUDIANTES
class Estudiante(db.Model):
    '''
    Clase: Estudiante
    Representa a cada uno de los estudiantes 

    Atributos:
        ID: Int, clave primaria
        Nombre: Str(30)
        Apellidos: Str(50)
        Curso: Int (1-6)
        Grado: Str(30) - Enum de grados?
        Titulo: 
        ¿ACEPTAR?
        ID_requisitos

    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "Estudiantes"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    apellidos = db.Column(db.String(50),nullable=False)
    curso = db.Column(db.Integer, nullable=False)
    grado = db.Column(db.String(30), nullable=False)
    # ID REQUISITOS
    id_requisitos = db.Column(db.Integer, ForeignKey("Requisitos.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    # asociado a la tabla auxiliar TITULO - ESTUDIANTE 
    titulo = db.relationship("Titulo", secondary=auxiliar_Titulo_Estudiantes, backref=backref('Estudiante', lazy='dynamic'), lazy='dynamic')
    

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,nombre,apellidos,curso,grado,titulo,id_requisito):
        self.nombre = nombre
        self.apellidos = apellidos
        self.curso = curso
        self.grado = grado
        self.titulo = titulo
        self.id_requisito = id_requisito

    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.apellidos}:{self.id}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Nombre":self.nombre, "Apellidos":self.apellidos, "Curso":self.curso, "Grado":self.grado, "Titulo":self.titulo, "Requisitos": self.id_requisito}

class EstudianteSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Estudiante
        include_relationships = True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        nombre = fields.String(required=True)
        apellidos = fields.String(required=True)
        curso = fields.Int(required=True)
        grado = fields.String(required=True)
        titulo = fields.List
        id_requisito = fields.Integer(required=True)



# ------------------------------------------------------------------------ ASIGNATURA ORIGEN 
class Asignatura_Origen(db.Model):
    '''
    Clase: Asignatura Origen

    Atributos:
        ID: Int, clave primaria
        nombre: de la asignatura
        codigo: de la asignatura, puede ser alfanumerico
        curso: en el que se cursa
        
    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "Asignatura_Origen"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    codigo = db.Column(db.String(50), nullable=False)
    curso = db.Column(db.Integer, nullable=False)


    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,nombre, codigo, curso):
        self.nombre = nombre
        self.codigo = codigo
        self.curso = curso
    
    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.nombre}:{self.id}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Id":self.id, "nombre":self.nombre, "codigo":self.codigo, "curso":self.curso}

class Asignatura_OrigenSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Asignatura_Origen
        include_relationships = True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        nombre = fields.String(required=True)
        codigo = fields.String(required=True)
        curso = fields.Integer(required=True)



# ------------------------------------------------------------------------ ASIGNATURA DESTINO
class Asignatura_Destino(db.Model):
    '''
    Clase: Asignatura Destino

    Atributos:
        ID: Int, clave primaria
        nombre: Str(30) universidad en la que se imparte
        codigo: de la asignatura
        ID_universidad: Int
        
    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "Asignatura_Destino"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    codigo = db.Column(db.String(50), nullable=False)
    # FOREIGN KEYS
    id_universidad = db.Column(db.Integer, ForeignKey("Universidad.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    universidad_id = relationship("Universidad", backref=backref("Asignatura_Destino"))
    

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,nombre, codigo,id_universidad):
        self.nombre = nombre
        self.codigo = codigo
        self.id_universidad = id_universidad
    

    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.nombre}:{self.id}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Id Asignatura Destino":self.id, "Nombre":self.nombre, "Codigo":self.codigo ,"Id_universidad":self.id_universidad}

class Asignatura_DestinoSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Asignatura_Destino
        include_relationships = True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        nombre = fields.String(required=True)
        codigo = fields.String(required=True)
        id_universidad = fields.Integer(required=True)
        



# ------------------------------------------------------------------------ ASIGNATURA DESTINO - ORIGEN 

class Asignatura_Destino_Asignatura_Origen(db.Model):
    '''
    Clase: Asignatura_Destino_Asignatura_Origen

    Atributos:
        ID: Int, clave primaria
        ID_Asignatura_destino: Int, clave foránea que hace referencia al id de la asignatura de destino
        ID_Asignatura_origen: Int, clave foránea que hace referencia al id de la asignatura de origen
        
    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "Asignatura_Destino_Asignatura_Origen"
    id = db.Column(db.Integer, primary_key=True)
    id_asignatura_origen = db.Column(db.Integer, ForeignKey("Asignatura_Origen.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    asignatura_origen = relationship("Asignatura_Origen", backref=backref("Asignatura_Destino_Asignatura_Origen"))
    id_asignatura_destino = db.Column(db.Integer, ForeignKey("Asignatura_Destino.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    asignatura_destino = relationship("Asignatura_Destino", backref=backref("Asignatura_Destino_Asignatura_Origen"))


    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self, id_asignatura_destino, id_asignatura_origen):
        self.id_asignatura_destino = id_asignatura_destino
        self.id_asignatura_origen = id_asignatura_origen
   

    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.id_asignatura_destino}:{self.id_asignatura_origen}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Id":self.id, "Id asignatura destino":self.id_asignatura_destino, "Id asignatura origen":self.id_asignatura_origen}

class Asignatura_Destino_Asignatura_OrigenSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Asignatura_Destino_Asignatura_Origen
        include_relationships = True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        id_asignatura_destino = fields.Number(required=True)
        id_asignatura_origen = fields.Number(required=True)




# ------------------------------------------------------------------------ LEARNING AGREEMENT
class LA(db.Model):
    '''
    Clase: Learning Agreement

    Atributos:
        ID: Int, clave primaria
        ID_estudiante: Int, clave foránea que se refiere al atributo id de la clase Estudiante
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
    id_estudiante = db.Column(db.Integer, db.ForeignKey("Estudiantes.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    estudiante = relationship("Estudiante", backref=backref("LA"))
    ceptado_RRII = db.Column(db.Boolean, default=False)
    aceptado_Coord = db.Column(db.Boolean, default=False)
    fdo_RRII = db.Column(db.Boolean, default=False)
    fdo_Coord = db.Column(db.Boolean, default=False)
    


    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,id_estudiante,aceptado_RRII,aceptado_Coord, fdo_RRII, fdo_Coord, listado_asignaturasOD):
        self.id_estudiante = id_estudiante  
        self.aceptado_RRII = aceptado_RRII
        self.aceptado_Coord = aceptado_Coord
        self.fdo_RRII = fdo_RRII
        self.fdo_Coord = fdo_Coord

    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.id}:{self.id_estudiante}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"ID_Estudiante":self.id_estudiante, "Aceptado RRII":self.aceptado_RRII,  "Aceptado Coord":self.aceptado_Coord, "Firmado RRII":self.fdo_RRII, "Firmado Coord":self.fdo_Coord, "id":self.id}

class LASchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = LA
        include_relationships= True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        id_estudiante = fields.Number(dump_only=True)
        aceptado_RRII = fields.Boolean(required=True)
        aceptado_Coord = fields.Boolean(required=True)
        fdo_RRII = fields.Boolean(required=True)
        fdo_Coord = fields.Boolean(required=True)



# ------------------------------------------------------------------------ ASOCIACION LA - ASIGNATURA 



# ------------------------------------------------------------------------ ENLACE ASIGNATURA DESTINO
class EnlaceAD(db.Model):
    '''
    Clase: EnlaceAD

    Atributos:
        ID: Int, clave primaria
        ID_Asignatura_destino: 
        año: 
        cuatri:
        link: 

    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "EnlaceAD"
    id = db.Column(db.Integer, primary_key=True)
    año = db.Column(db.Integer, nullable=False)
    link = db.Column(db.String(255), nullable=False)
    cuatri = db.Column(db.Integer, nullable=False)
    id_asignatura_destino = db.Column(db.Integer, ForeignKey("Asignatura_Destino.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    asignatura_destino = relationship("Asignatura_Destino", backref=backref("EnlaceAD"))

    
    
    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,año,link, cuatri, id_asignatura_destino):
        self.año = año
        self.link = link
        self.cuatri = cuatri
        self.id_asignatura_destino = id_asignatura_destino
        
    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.id_asignatura_destino}:{self.link}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"ID asignatura Destino":self.id_asignatura_destino, "año":self.año, "cuatri": self.cuatri, "link":self.link}

class EnlaceADSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = EnlaceAD
        include_relationships = True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        id_asignatura_destino = fields.Number(required=True)
        año = fields.Number(required=True)
        cuatri = fields.Number(required=True)
        link = fields.String(required=True)


#las auxiliares estan en prueba.py
db.drop_all()
# aqui estaria bien meter algo de codigo para que se ejecutase el workflow de pruebas de postman
# y despues los inserts a cada una de las tablas auxiliares
db.create_all()