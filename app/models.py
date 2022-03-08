
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


class Estudiante(db.Model):
    '''
    Clase: Estudiante

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
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        confirmacion = fields.Integer(required=True)
        año = fields.Integer(required=True)
        cuatri = fields.Integer(required=True)
        vuelta = fields.Integer(required=True)



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
    id_asignatura_d = db.Column(db.Integer, ForeignKey("Asignatura_Destino.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    #asignatura_destino = relationship("Asignatura_Destino", foreign_keys=[id_asignatura_d])
    #children = relationship("Child")

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,nombre,ubicacion, plazas, id_asignatura_d):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.plazas = plazas
        self.id_asignatura_d = id_asignatura_d

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
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        nombre = fields.String(required=True)
        ubicacion = fields.String(required=True)
        id_asignatura_destino = fields.Integer(required=True)
        


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
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        


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

class Asignatura_Destino_Asignatura_Origen(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Asignatura_Destino_Asignatura_Origen
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        id_asignatura_destino = fields.Number(dump_only=True)
        id_asignatura_origen = fields.Number(dump_only=True)



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
    #student = relationship("Estudiante", backref='children')
    #estudiante = relationship("Estudiante", backref="LA")
    #subjects = relationship('Asignatura_Destino_Asignatura_Origen', secondary='AOD_LA')

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
        #print(model.id_estudiante)
        include_relationships= True
        sqla_session = db.session
        id = fields.Number(dump_only=True)
        id_estudiante = fields.Number(dump_only=True)
        aceptado_RRII = fields.Boolean(required=True)
        aceptado_Coord = fields.Boolean(required=True)
        fdo_RRII = fields.Boolean(required=True)
        fdo_Coord = fields.Boolean(required=True)


#Estudiante.LA = relationship("LA", order_by = LA.id, back_populates = "estudiante")


# AUXILIAR ESTUDIANTE - SELECCION
class Estudiante_Seleccion(db.Model):
    '''
    Clase: Estudiante_Seleccion
    Tabla auxiliar que se debe generar debido a la relacion N:M entre las entidades de Estudiante y Seleccion

    Atributos:
        ID_estudiante: Int, clave foranea que hace referencia al id de la clase estudiante
        ID_seleccion: Int, clave foranea que hace referencia al id de la clase seleccion
        Plaza: Str(30)
        Aceptar: Bool
        
    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "Estudiantes-Seleccion"
    id_estudiante = db.Column(db.Integer, ForeignKey("Estudiantes.id"), primary_key=True)
    id_seleccion = db.Column(db.Integer, ForeignKey("Seleccion.id"), primary_key=True)
    plaza = db.Column(db.String(30), nullable=False)
    aceptar = db.Column(db.Boolean(50), nullable=False)
    

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,id_estudiante,id_seleccion, plaza,aceptar):
        self.id_estudiante = id_estudiante
        self.id_seleccion = id_seleccion
        self.plaza = plaza
        self.aceptar = aceptar

    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.id_estudiante}:{self.id_seleccion}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Id_Estudiante":self.id_estudiante, "ID_Seleccion":self.id_seleccion, "Plaza":self.plaza, "Aceptado":self.aceptar}

class Estudiante_SeleccionSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Estudiante_Seleccion
        sqla_session = db.session
        id_seleccion = fields.Number(dump_only=True)
        id_estudiante = fields.Number(dump_only=True)
        plaza = fields.Str(required=True)
        aceptar = fields.Boolean(required=True)
       


# AUXILIAR SELECCION - UNIVERSIDAD DE DESTINO
class Seleccion_Universidad(db.Model):
    '''
    Clase: Estudiante_Universidad
    Tabla auxiliar que se debe generar debido a la relacion N:M entre las entidades de Seleccion y Universidad de Destino

    Atributos:
        ID_universidad: Int, clave foranea que hace referencia al id de la clase universidad, junto con id_seleccion configuran la clave primaria
        ID_seleccion: Int, clave foranea que hace referencia al id de la clase seleccion, junto con id_universidad configuran la clave primaria

        
    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "Seleccion-Universidad"
    id_universidad = db.Column(db.Integer, ForeignKey("Universidad.id"), primary_key=True)
    id_seleccion = db.Column(db.Integer, ForeignKey("Seleccion.id"), primary_key=True)

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,id_universidad,id_seleccion):
        self.id_universidad = id_universidad
        self.id_seleccion = id_seleccion


    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        return f"{self.id_universidad}:{self.id_seleccion}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"Id":self.id, "Id_Seleccion":self.id_seleccion, "Id_Universidad":self.id_universidad}

class Seleccion_UniversidadSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Seleccion_Universidad
        sqla_session = db.session
        id_seleccion = fields.Number(dump_only=True)
        id_universidad = fields.Number(dump_only=True)
       

# AUXILIAR LA - ASIGNATURA_DESTINO_ASIGNATURA_ORIGEN
class AsignaturaOD_LA(db.Model):
    '''
    Clase: AsignaturaOD_LA
    Tabla auxiliar que se debe generar debido a la relacion N:M entre las entidades de Asignatura_Origen_Asignatura_Destino y LA

    Atributos:
        ID_AOD: Int, clave foranea que hace referencia al id de la clase Asignatura_Destino_asignatura_Origen, junto con id_LA configuran la clave primaria
        ID_LA: Int, clave foranea que hace referencia al id de la clase LA, junto con id_AOD configuran la clave primaria

        
    Funciones
        def create(self)
        def __init__
        def __repr__
        def json(self)
    '''
    __tablename__ = "AOD_LA"
    id_AOD = db.Column(db.Integer, ForeignKey("Asignatura_Destino_Asignatura_Origen.id"), primary_key=True)
    id_LA = db.Column(db.Integer, ForeignKey("LA.id"), primary_key=True)

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self,id_AOD,id_LA):
        self.id_AOD = id_AOD
        self.id_LA = id_LA


    def __repr__(self):
        '''
        repr method represents how one onject will look like
        '''
        #return f"{self.apellidos}:{self.id}"

    def json(self):
        '''
        Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
        '''
        return {"ID_LA":self.id_LA, "ID_AOD":self.id_AOD}

class AsignaturaOD_LASchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = AsignaturaOD_LA
        sqla_session = db.session
        id_AOD = fields.Number(dump_only=True)
        id_LA = fields.Number(dump_only=True)


#Estudiante.learning_agreemts = db.relationship('LA', backref='Estudiantes', lazy=True)

db.create_all()