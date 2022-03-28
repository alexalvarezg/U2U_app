
from __future__ import unicode_literals
from ast import dump
from tkinter.tix import Tree
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from . import db
#from app import db



#db.drop_all()
#Base = declarative_base()

#Establecemos las tablas auxiliares

## ESTUDIANTE - SELECCION 
auxiliar_estudiante_seleccion = db.Table('aux_estudiante_seleccion', 
    db.Column('id_estudiante', db.Integer, db.ForeignKey('Estudiantes.id'), primary_key=True), 
    db.Column('id_seleccion', db.Integer, db.ForeignKey('Seleccion.id'), primary_key = True), 
    db.Column('plazas', db.Integer, nullable=False), 
    db.Column('aceptar', db.Boolean, nullable=False)
)

## UNIVERSIDAD - SELECCION
auxiliar_universidad_seleccion = db.Table('aux_universidad_seleccion', 
    db.Column('id_universidad', db.Integer, db.ForeignKey('Universidad.id'), primary_key=True), 
    db.Column('id_seleccion', db.Integer, db.ForeignKey('Seleccion.id'), primary_key = True)
)


## LA - ASIGNATURA_DESTINO_ORIGEN
auxiliar_LA_asignaturasOD = db.Table('aux_LA_asignaturasOD', 
    db.Column('id_AOD', db.Integer, db.ForeignKey('Asignatura_Destino_Asignatura_Origen.id'), primary_key=True), 
    db.Column('id_LA', db.Integer, db.ForeignKey('LA.id'), primary_key = True)
)

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
        Titulo: ---- no se como poner esto porque podría ser una lista o diccionario que tenga varios idiomas y un si o no y nivel ---

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
    titulo = db.Column(db.String(30), nullable=False)
    # Representar la relacion del LA
    #learning_agreemts = db.relationship('LA', backref='Estudiantes', lazy=True)
    # Representar la relacion de las selecciones

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
        titulo = fields.String(required=True)

'''#association table para las asignaturas, la relacion esta exxpresada en la entidad Asignatura de destino
asignaturas_origen_destino = db.Table('asignaturas_origen_destino', 
    db.Column('asignatura_origen_id', db.Integer, db.ForeignKey('Asignatura_Origen.id')), 
    db.Column('asignatura_destino_id', db.Integer, db.ForeignKey('Asignatura_Destino.id'))
)
'''


class Asignatura_Origen(db.Model):
    '''
    Clase: Asignatura Origen

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
    nombre = db.Column(db.String(255), nullable=False)


    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,nombre):
        self.nombre = nombre
    
    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.nombre}:{self.id}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Id":self.id, "nombre":self.nombre}

class Asignatura_OrigenSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Asignatura_Origen
        include_relationships = True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        nombre = fields.String(required=True)
        


class Asignatura_Destino(db.Model):
    '''
    Clase: Asignatura Destino

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
    nombre = db.Column(db.String(255), nullable=False)
    id_universidad = db.Column(db.Integer, ForeignKey("Universidad.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    universidad_id = relationship("Universidad", backref=backref("Asignatura_Destino"))
    

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,nombre):
        self.nombre = nombre
    

    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.nombre}:{self.id}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Id Asignatura Destino":self.id, "Nombre":self.nombre}

class Asignatura_DestinoSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Asignatura_Destino
        include_relationships = True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        


class Universidad(db.Model):
    '''
    Clase: Universidad

    Atributos:
        ID: Int, clave primaria
        Nombre: Str(30) Nombre de la universidad de destino
        Ubicación: Str(50) País y ciudad
        plazas: numero de plazas disponibles en la universidad
        id_asignatura_destino: clave foranea que hace referencia al id de la asignatura de destino
        
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
    plazas = db.Column(db.Integer, nullable=True) #puede que no haya plazas
    
    
    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,nombre,ubicacion, plazas, id_asignatura_d):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.plazas = plazas

    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.nombre}:{self.id}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Nombre":self.nombre, "Ubicación":self.ubicacion, "Plazas":self.plazas, "Asignatura Destino":self.id_asignatura_d}

class UniversidadSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Universidad
        include_relationships = True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        nombre = fields.String(required=True)
        ubicacion = fields.String(required=True)
        id_asignatura_destino = fields.Integer(required=True)
  


class Seleccion(db.Model):
    '''
    Clase: Seleccion

    Atributos:
        Id_seleccion: Int clave primaria
        año: Int() ---- podria ponerse formato datetime
        cuatri: Int (1-2)
        vuelta: Int (1-2)
        confirmacion: clave foranea, hace referencia al id de la universidad de destino

    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "Seleccion"
    id = db.Column(db.Integer, primary_key=True)
    cuatri = db.Column(db.Integer, nullable=False)
    año = db.Column(db.Integer, nullable=False)
    vuelta = db.Column(db.Integer, nullable=False)
    confirmacion = db.Column(db.Integer, ForeignKey("Universidad.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    universidad = relationship("Universidad", backref=backref("Seleccion"))
    estudiantes = db.relationship("Estudiante", secondary=auxiliar_estudiante_seleccion)
    universidades = db.relationship("Universidad", secondary=auxiliar_universidad_seleccion)

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,confirmacion, cuatri, año, vuelta):
        self.cuatri = cuatri
        self.año = año
        self.vuelta = vuelta
        self.confirmacion = confirmacion

    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.id}:{self.año}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Año":self.año, "Cuatrimestre":self.cuatri, "Vuelta":self.vuelta, "Confirmacion":self.confirmaciones}

class SeleccionSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Seleccion
        include_relationships = True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        confirmacion = fields.Integer(required=True)
        año = fields.Integer(required=True)
        cuatri = fields.Integer(required=True)
        vuelta = fields.Integer(required=True)



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
    id_asignatura_destino = db.Column(db.Integer, ForeignKey("Asignatura_Destino.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    origen = relationship("Asignatura_Origen", backref=backref("Asignatura_Destino_Asignatura_Origen"))
    destino = relationship("Asignatura_Destino", backref=backref("Asignatura_Destino_Asignatura_Origen"))
    #la = relationship('LA', secondary='AOD_LA') #en este caso LA va entre '' porque no esta aun creada la clase LA


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
    aceptado_RRII = db.Column(db.Boolean, default=False)
    aceptado_Coord = db.Column(db.Boolean, default=False)
    fdo_RRII = db.Column(db.Boolean, default=False)
    fdo_Coord = db.Column(db.Boolean, default=False)
    estudiante = relationship("Estudiante", backref=backref("LA"))
    asignaturasOD = db.relationship("Asignatura_Destino_Asignatura_Origen", secondary=auxiliar_LA_asignaturasOD)

    

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,id_estudiante,aceptado_RRII,aceptado_Coord, fdo_RRII, fdo_Coord):
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



#las auxiliares estan en prueba.py

#db.create_all()