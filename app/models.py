from __future__ import unicode_literals

from tkinter.tix import Tree
from unicodedata import name
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import ForeignKey, Table, Column, false
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from . import db

from sqlalchemy import UniqueConstraint

from sqlalchemy import insert




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


## TITULACIONES - UNIVERSIDAD DE DESTINO
auxiliar_titulacion_universidad = db.Table('aux_titulacion_universidad', 
    db.Column('id_universidad', db.Integer, db.ForeignKey('Universidad.id'), primary_key=True), 
    db.Column('id_titulacion', db.Integer, db.ForeignKey('Titulaciones.id'), primary_key=True)
)

## ASIGNATURAS ORIGEN - TITULACIONES
auxiliar_titulacion_asignaturasO = db.Table('aux_titulacion_asignaturas_O', 
    db.Column('id_asignatura_O', db.Integer, db.ForeignKey('Asignatura_Origen.id'), primary_key=True), 
    db.Column('id_titulacion', db.Integer, db.ForeignKey('Titulaciones.id'), primary_key=True)
)






'''
ENTIDADES - SEGURIDAD
'''
# ------------------------------------------------------------------------ USUARIO
class User(db.Model):
    '''
    Clase: Usuario

    Atributos:
        ID: Int, clave primaria
        nombre: Str, nombre de usuario con el que quiere registrarse y posteriormente iniciar sesion 
        email: Str, direccion de correo electronico asocida al usuario
        password: Str, contraseña de acceso a la interfaz

    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "users"
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
    Esta entidad recoge los idiomas y niveles que pueden ser presentados por un alumno y exigidos por la universidad de destino. 
    
    Atributos:
        ID: Int, clave primaria
        idioma: Str, diferentes idiomas existentes como ingles, aleman etc. cada valor lleva asociado un idioma concreto
        nivel: Str, diferentes niveles para cada idioma, cada valor lleva asociado un nivel concreto
        tipo: Str, diferente tipo, cada valor lleva asociado un tipo concreto
        puntuacion: Int, diferenciando entre 0, 10, 20 y 30 posibles puntos
        
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




# ------------------------------------------------------------------------ TITULACIONES UNIVERSITARIAS
class Titulacion(db.Model):
    '''
    Clase: Titulacion
    Esta entidad hace referencia a la oferta académica que se puede encontrar en la Escuela Politécnica Superior del CEU asociada a los grados de ingeniería y arquitectura. 

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
    nombre = db.Column(db.String(100), nullable=False)
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


# ------------------------------------------------------------------------ UNIVERSIDAD DE DESTINO
class Universidad(db.Model):
    '''
    Clase: Universidad
    Esta entidad representa, como su nombre indica, a la universidad de destino a la cual se marcharía el alumno en el caso de haber completado el proceso de movilidad de manera satisfactoria. 

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
    nombre = db.Column(db.String(100), nullable=False)
    ubicacion = db.Column(db.String(50), nullable=False)
    plazas1 = db.Column(db.Integer, nullable=True) 
    plazas2 = db.Column(db.Integer, nullable=True) 
    # asociado a la tabla auxiliar TITULO - UNIVERSIDAD
    titulo = db.relationship("Titulo", secondary=auxiliar_Titulo_Universidad, backref=backref('Universidad', lazy='dynamic'), lazy='dynamic')
    # asociado a la tabla auxiliar TITULACIONES - UNIVERSIDAD
    titulaciones = db.relationship("Titulacion", secondary=auxiliar_titulacion_universidad, backref=backref('Universidad', lazy='dynamic'), lazy='dynamic')

    
    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,nombre,ubicacion, plazas1, plazas2,titulo, titulaciones):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.plazas1 = plazas1
        self.plazas2 = plazas2
        self.titulo = titulo
        self.titulaciones = titulaciones

    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.nombre}:{self.id}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Nombre":self.nombre, "Ubicación":self.ubicacion, "Plazas primer cuatri":self.plazas1, "Plazas segundo cuatri":self.plazas2,"Titulo": self.titulo, "Titulaciones": self.titulaciones}

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
        titulaciones = fields.List




# ------------------------------------------------------------------------ REQUISITOS
class Requisitos(db.Model):
    '''
    Clase: Requisitos

    Atributos:
        ID: Int, clave primaria
        nombre: Str, descripcion del requisito en si
        
    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "Requisitos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(55), nullable=True)
    


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

class RequisitosSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Requisitos
        include_relationships = True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        nombre = fields.String(required=True)
       





# ------------------------------------------------------------------------ ESTUDIANTES
class Estudiante(db.Model):
    '''
    Clase: Estudiante
    Representa a cada uno de los estudiantes 

    Atributos:
        ID: Int, clave primaria
        Nombre: Str(30), nombre del estudiante
        Apellidos: Str(50), apellidos del estudiante
        Curso: Int (1-6), curso academico en el que se encuentra el estudiante
        Grado: Str(30), diferentes grados posibles
        Titulo: certificado de idioma asociado al estudiante
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

    def __init__(self,nombre, apellidos, curso, grado, titulo, id_requisitos):
        self.nombre = nombre
        self.apellidos = apellidos
        self.curso = curso
        self.grado = grado
        self.titulo = titulo
        self.id_requisitos = id_requisitos


    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.apellidos}:{self.id}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Nombre":self.nombre, "Apellidos":self.apellidos, "Curso":self.curso, "Grado":self.grado, "Titulo":self.titulo, "Requisitos": self.id_requisitos}

class EstudianteSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Estudiante
        include_relationships = True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        nombre = fields.String(required=True)
        apellidos = fields.String(required=True)
        curso = fields.Number(required=True)
        grado = fields.String(required=True)
        titulo = fields.List
        id_requisitos = fields.Number(required=True)
        




# ------------------------------------------------------------------------ PRE SELECCION (ASSOCIATION TABLE)
class PreSeleccion(db.Model):
    '''
    Clase: Pre Selecccion
    
    Atributos:
        id: Int, clave primaria
        año: Int, año en el que se va a realizar la movilidad
        orden: Str, orden de preferencia de las universidades de destino pre-seleccionadas
        cuatri: Int, cuatrimestre que se marcharia

    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "PreSeleccion"
    id_estudiante = db.Column(db.Integer, ForeignKey("Estudiantes.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    estudiante = db.relationship("Estudiante", backref=backref("Preseleccion"))
    id_universidad = db.Column(db.Integer, ForeignKey("Universidad.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    universidad = db.relationship("Universidad", backref=backref("Preseleccion"))

    id = db.Column(db.Integer, primary_key=True)
    año = db.Column(db.Integer, nullable=False)
    orden = db.Column(db.String(155),nullable=False) #¿?
    cuatri = db.Column(db.Integer, nullable=False)


    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,id_estudiante, id_universidad, año, cuatri, orden):
        self.id_estudiante = id_estudiante
        self.id_universidad = id_universidad
        self.año = año
        self.orden = orden
        self.cuatri = cuatri
        

    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.id_estudiante}:{self.id_universidad}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Id Estudiante":self.id_estudiante, "Id Universidad":self.id_universidad, "Año":self.año, "Orden":self.orden, "Cuatri":self.cuatri}

class PreSeleccionSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = PreSeleccion
        include_relationships = True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        id_estudiante = fields.Integer(required=True)
        id_universidad = fields.Integer(required=True)
        año = fields.Integer(required=True)
        cuatri = fields.Integer(required=True)
        orden = fields.List



# ------------------------------------------------------------------------ SELECCION (ASSOCIATION TABLE)
class Seleccion(db.Model):
    '''
    Clase: Selecccion
    
    Atributos:
        id: Int, clave primaria
        año: Int, año en el que realizaría el proceso de movilidad
        cuatri: Int, cuatrimestre que se marcharia de movilidad
        vuelta: Int, vuelta en la que escogio su plaza finalmente

    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "Seleccion"
    id_estudiante = db.Column(db.Integer, ForeignKey("Estudiantes.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    estudiante = db.relationship("Estudiante", backref=backref("Seleccion"))
    id_universidad = db.Column(db.Integer, ForeignKey("Universidad.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    universidad = db.relationship("Universidad", backref=backref("Seleccion"))

    id = db.Column(db.Integer, primary_key=True)
    año = db.Column(db.Integer, nullable=False)
    cuatri = db.Column(db.Integer, nullable=False)
    vuelta = db.Column(db.Integer, nullable=False)



    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,id_estudiante, id_universidad, año, cuatri, vuelta):
        self.id_estudiante = id_estudiante
        self.id_universidad = id_universidad
        self.año = año
        self.vuelta = vuelta
        self.cuatri = cuatri
        

    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.id_estudiante}:{self.id_universidad}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Id Estudiante":self.id_estudiante, "Id Universidad":self.id_universidad, "Año":self.año, "Vuelta":self.vuelta, "Cuatri":self.cuatri}

class SeleccionSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Seleccion
        include_relationships = True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        id_estudiante = fields.Integer(required=True)
        id_universidad = fields.Integer(required=True)
        año = fields.Integer(required=True)
        cuatri = fields.Integer(required=True)
        vuelta = fields.Integer(required=True)






# ------------------------------------------------------------------------ ASIGNATURA ORIGEN 
class Asignatura_Origen(db.Model):
    '''
    Clase: Asignatura Origen
    Esta entidad hace referencia a la asignatura que el alumno cursaría en la universidad CEU San Pablo si se quedase, y la cual estaría convalidando en el LA por otra(s) asignatura(s) en la universidad de destino. 

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
    # asociado a la tabla auxiliar TITULACIONES - UNIVERSIDAD
    titulaciones = db.relationship("Titulacion", secondary=auxiliar_titulacion_asignaturasO, backref=backref('Asignatura_Origen', lazy='dynamic'), lazy='dynamic')

    
    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,nombre, codigo, curso, titulaciones):
        self.nombre = nombre
        self.codigo = codigo
        self.curso = curso
        self.titulaciones = titulaciones
    
    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.nombre}:{self.id}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Id":self.id, "nombre":self.nombre, "codigo":self.codigo, "curso":self.curso, "Titulaciones": self.titulaciones}

class Asignatura_OrigenSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Asignatura_Origen
        include_relationships = True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        nombre = fields.String(required=True)
        codigo = fields.String(required=True)
        curso = fields.Integer(required=True)
        titulaciones = fields.List



# ------------------------------------------------------------------------ ASIGNATURA DESTINO
class Asignatura_Destino(db.Model):
    '''
    Clase: Asignatura Destino
    Esta entidad hace referencia a la asignatura que el alumno cursará en la universidad de destino en sustitución de la asignatura que cursaría en la universidad CEU San Pablo si se quedase. 

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
    Esta entidad surge como consecuencia de una relación ternaria entre Asignatura de destino y asignatura de origen. 

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
    Esta entidad representa el acuerdo que se establece entre el alumno, la universidad de origen y la universidad de destino para cuadrar las asignaturas que el alumno cursará en la universidad de destino durante su proceso de movilidad y que quede constancia de ello y puedan ser convalidadas una vez regrese a su universidad de origen (y cumpla el resto de los requisitos establecidos, como la firma de la carta Erasmus etc.) 

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
    aceptado_RRII = db.Column(db.Boolean, default=False)
    aceptado_Coord = db.Column(db.Boolean, default=False)
    fdo_RRII = db.Column(db.Boolean, default=False)
    fdo_Coord = db.Column(db.Boolean, default=False)
    


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



# ------------------------------------------------------------------------ ASOCIACION LA - ASIGNATURA 
class AsociacionLA_A(db.Model):
    '''
    Clase: AsociacionLA_A

    Atributos:
        ID: Int, clave primaria
        ID_reflexivo: su propio id como consecuencia de la relacion reflexiva (1,N) 
        cancelado: Bool, indica si el LA ha sido o no cancelado
        fecha cancelacion: Date, indica la fecha en la que ha sido cancelado
        motivo: Str, motivo por el cual se ha cancelado
        aceptado: Bool, indica si el La esta aceptado o no
        fecha aceptacion: Date, fecha en la que se acepto el LA
        id_La: clave foránea que representa el id del LA
        id_asignatura_origen_destino: clave foránea que representa el id del conjunto asignatura destino - origen

    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "AsociacionLA_A"
    id = db.Column(db.Integer, primary_key=True)
    cancelado = db.Column(db.Boolean, default=False)
    fecha_cancelacion = db.Column(db.Date , nullable=True)
    motivo = db.Column(db.String(255), nullable=True)
    aceptado = db.Column(db.Boolean, default=False)
    fecha_aceptacion = db.Column(db.Date, nullable=True)
    id_LA = db.Column(db.Integer, ForeignKey("LA.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    learnign_agreement = relationship("LA", backref=backref("AsociacionLA_A"))
    id_asignatura_OD = db.Column(db.Integer, ForeignKey("Asignatura_Destino_Asignatura_Origen.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    asignatura_destino_origen = relationship("Asignatura_Destino_Asignatura_Origen", backref=backref("AsociacionLA_A"))
    
    
    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,cancelado, fecha_cancelacion, motivo, aceptado, fecha_aceptacion ,id_LA, id_asignatura_OD):
        self.cancelado = cancelado
        self.fecha_cancelacion = fecha_cancelacion
        self.motivo = motivo 
        self.aceptado = aceptado
        self.fecha_aceptacion = fecha_aceptacion
        self.id_LA = id_LA
        self.id_asignatura_OD = id_asignatura_OD
        
        
    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.id}:{self.aceptado}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Id":self.id, "Cancelado":self.cancelado, "Fecha Cancelacion": self.fecha_cancelacion, "Motivo":self.motivo, "Aceptado":self.aceptado, "Fecha Aceptacion": self.fecha_aceptacion, "ID Learning Agreement": self.id_LA, "ID Asignatura OD": self.id_asignatura_OD}

class AsociacionLA_ASchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = AsociacionLA_A
        include_relationships = True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        cancelado = fields.Boolean(required=True)
        fecha_cancelacion = fields.DateTime(required=False)
        motivo = fields.String(required=False)
        aceptado = fields.Boolean(required=True)
        fecha_aceptacion = fields.DateTime(required=False)
        id_LA = fields.Integer(required=True)
        id_asignatura_OD = fields.Integer(required=True)

       

# ------------------------------------------------------------------------ ENLACE ASIGNATURA DESTINO
class EnlaceAD(db.Model):
    '''
    Clase: EnlaceAD
    Esta entidad refleja un histórico de los posibles cambios que pueda experimentar una asignatura en la universidad de destino.

    Atributos:
        ID: Int, clave primaria
        ID_Asignatura_destino: 
        año: Int, año en el que se cursaria dicha asignatura
        cuatri: Int, cuatrimestre en el que se cursaria dicha asignatura
        link: Str, enlace a la guia docente de la asignatura

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

#para pruebas
#db.drop_all()
#db.create_all()