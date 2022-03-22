prueba = [
    {
      "nombre": "Alejandro", 
      "apellidos": "Alvarez Gallardo", 
      "curso": 4, 
      "grado": "GIT", 
      "titulo": "InglesC1"
    }, 
    {
      "nombre": "Ana", 
      "apellidos": "Cerro Garcia", 
      "curso": 4, 
      "grado": "GIT", 
      "titulo": "InglesB2"
    }, 
    {
      "nombre": "Diego", 
      "apellidos": "del Rio", 
      "curso": 4, 
      "grado": "GIT", 
      "titulo": "InglesB2"
    }, 
    {
      "nombre": "Eduardo", 
      "apellidos": "Efosa Edokpolor", 
      "curso": 4, 
      "grado": "GIT", 
      "titulo": "InglesC1"
    }, 
    {
      "nombre": "Eugenia", 
      "apellidos": "Ortega", 
      "curso": 4, 
      "grado": "GIT", 
      "titulo": "InglesC2"
    }, 
    {
      "nombre": "Javier", 
      "apellidos": "Valero", 
      "curso": 4, 
      "grado": "GIT", 
      "titulo": "InglesC1"
    }, 
    {
      "nombre": "Jose", 
      "apellidos": "Garcia", 
      "curso": 4, 
      "grado": "GIT", 
      "titulo": "InglesB2"
    }, 
    {
      "nombre": "Lucas", 
      "apellidos": "Encinas Sabater", 
      "curso": 4, 
      "grado": "GIT", 
      "titulo": "InglesC2"
    }, 
    {
      "nombre": "Martin", 
      "apellidos": "Cordero", 
      "curso": 4, 
      "grado": "GIT", 
      "titulo": "InglesC2"
    }, 
    {
      "nombre": "Clara", 
      "apellidos": "Esteban", 
      "curso": 4, 
      "grado": "GIT", 
      "titulo": "InglesB2"
    }
  ]

print(prueba[0]["nombre"])

for i in range(1, len(prueba)):
    print(prueba[i]["nombre"])



# # AUXILIAR ESTUDIANTE - SELECCION
# class Estudiante_Seleccion(db.Model):
#     '''
#     Clase: Estudiante_Seleccion
#     Tabla auxiliar que se debe generar debido a la relacion N:M entre las entidades de Estudiante y Seleccion

#     Atributos:
#         ID_estudiante: Int, clave foranea que hace referencia al id de la clase estudiante
#         ID_seleccion: Int, clave foranea que hace referencia al id de la clase seleccion
#         Plaza: Str(30)
#         Aceptar: Bool
        
#     Funciones
#         def create(self)
#         def __init__
#         def __repr__
#         def json(self)
#     '''
#     __tablename__ = "Estudiantes-Seleccion"
#     id_estudiante = db.Column(db.Integer, ForeignKey("Estudiantes.id"), primary_key=True)
#     id_seleccion = db.Column(db.Integer, ForeignKey("Seleccion.id"), primary_key=True)
#     plaza = db.Column(db.String(30), nullable=False)
#     aceptar = db.Column(db.Boolean(50), nullable=False)
#     estudiante = relationship("Estudiante", backref=backref("Estudiantes-Seleccion"))
#     seleccion = relationship("Seleccion", backref=backref("Estudiantes-Seleccion"))

#     def create(self):
#       db.session.add(self)
#       db.session.commit()
#       return self

#     def __init__(self,id_estudiante,id_seleccion, plaza,aceptar):
#         self.id_estudiante = id_estudiante
#         self.id_seleccion = id_seleccion
#         self.plaza = plaza
#         self.aceptar = aceptar

#     def __repr__(self):
#         '''
#         repr method represents how one onject will look like
#         '''
#         return f"{self.id_estudiante}:{self.id_seleccion}"

#     def json(self):
#         '''
#         Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
#         '''
#         return {"Id_Estudiante":self.id_estudiante, "ID_Seleccion":self.id_seleccion, "Plaza":self.plaza, "Aceptado":self.aceptar}

# class Estudiante_SeleccionSchema(SQLAlchemyAutoSchema):
#     class Meta(SQLAlchemyAutoSchema.Meta):
#         model = Estudiante_Seleccion
#         include_relationships = True
#         sqla_session = db.session
#         id_seleccion = fields.Number(dump_only=True)
#         id_estudiante = fields.Number(dump_only=True)
#         plaza = fields.Str(required=True)
#         aceptar = fields.Boolean(required=True)
       

# # AUXILIAR SELECCION - UNIVERSIDAD DE DESTINO
# class Seleccion_Universidad(db.Model):
#     '''
#     Clase: Estudiante_Universidad
#     Tabla auxiliar que se debe generar debido a la relacion N:M entre las entidades de Seleccion y Universidad de Destino

#     Atributos:
#         ID_universidad: Int, clave foranea que hace referencia al id de la clase universidad, junto con id_seleccion configuran la clave primaria
#         ID_seleccion: Int, clave foranea que hace referencia al id de la clase seleccion, junto con id_universidad configuran la clave primaria

        
#     Funciones
#         def create(self)
#         def __init__
#         def __repr__
#         def json(self)
#     '''
#     __tablename__ = "Seleccion-Universidad"
#     id_universidad = db.Column(db.Integer, ForeignKey("Universidad.id"), primary_key=True)
#     id_seleccion = db.Column(db.Integer, ForeignKey("Seleccion.id"), primary_key=True)
#     universidad_id = relationship("Universidad", backref=backref("Seleccion-Universidad"))
#     seleccion_id = relationship("Seleccion", backref=backref("Seleccion-Universidad"))

#     def create(self):
#       db.session.add(self)
#       db.session.commit()
#       return self

#     def __init__(self,id_universidad,id_seleccion):
#         self.id_universidad = id_universidad
#         self.id_seleccion = id_seleccion


#     def __repr__(self):
#         '''
#         repr method represents how one onject will look like
#         '''
#         return f"{self.id_universidad}:{self.id_seleccion}"

#     def json(self):
#         '''
#         Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
#         '''
#         return {"Id":self.id, "Id_Seleccion":self.id_seleccion, "Id_Universidad":self.id_universidad}

# class Seleccion_UniversidadSchema(SQLAlchemyAutoSchema):
#     class Meta(SQLAlchemyAutoSchema.Meta):
#         model = Seleccion_Universidad
#         include_relationships = True
#         sqla_session = db.session
#         id_seleccion = fields.Number(dump_only=True)
#         id_universidad = fields.Number(dump_only=True)
       

# # AUXILIAR LA - ASIGNATURA_DESTINO_ASIGNATURA_ORIGEN
# class AsignaturaOD_LA(db.Model):
#     '''
#     Clase: AsignaturaOD_LA
#     Tabla auxiliar que se debe generar debido a la relacion N:M entre las entidades de Asignatura_Origen_Asignatura_Destino y LA

#     Atributos:
#         ID_AOD: Int, clave foranea que hace referencia al id de la clase Asignatura_Destino_asignatura_Origen, junto con id_LA configuran la clave primaria
#         ID_LA: Int, clave foranea que hace referencia al id de la clase LA, junto con id_AOD configuran la clave primaria

        
#     Funciones
#         def create(self)
#         def __init__
#         def __repr__
#         def json(self)
#     '''
#     __tablename__ = "AOD_LA"
#     id_AOD = db.Column(db.Integer, ForeignKey("Asignatura_Destino_Asignatura_Origen.id"), primary_key=True)
#     id_LA = db.Column(db.Integer, ForeignKey("LA.id"), primary_key=True)
#     asingaturas_relacion = relationship("Asignatura_Destino_Asignatura_Origen", backref=backref("AOD_LA"))
#     Learning_Agreement_id = relationship("LA", backref=backref("AOD_LA"))

#     def create(self):
#       db.session.add(self)
#       db.session.commit()
#       return self

#     def __init__(self,id_AOD,id_LA):
#         self.id_AOD = id_AOD
#         self.id_LA = id_LA


#     def __repr__(self):
#         '''
#         repr method represents how one onject will look like
#         '''
#         return f"{self.id_AOD}:{self.id_LA}"

#     def json(self):
#         '''
#         Como las apis funcionan con JSON, creamos un metodo .json para que devuelva un json product object
#         '''
#         return {"ID_LA":self.id_LA, "ID_AOD":self.id_AOD}

# class AsignaturaOD_LASchema(SQLAlchemyAutoSchema):
#     class Meta(SQLAlchemyAutoSchema.Meta):
#         model = AsignaturaOD_LA
#         include_relationships = True
#         sqla_session = db.session
#         id_AOD = fields.Number(dump_only=True)
#         id_LA = fields.Number(dump_only=True)
