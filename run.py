from app import app
from app.models import Estudiante, EstudianteSchema
'''
    Informacion extra
    
    estudiante_schema = EstudianteSchema()
    estudiantes = Estudiante(nombre="Alejandro" , apellidos="Alvarez Gallardo", curso=4, grado="GIT", titulo="InglesC1")
    print("Estructura de un Estudiante" + "\n" + str(estudiante_schema.dump(estudiantes))) #muestra la estructura de estudiantes
'''

if __name__ == "__main__":
    app.run()