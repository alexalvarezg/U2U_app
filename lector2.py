import pandas as pd
from pandas import read_excel

'''
https://naps.com.mx/blog/uso-de-query-con-pandas-en-python/

'''

# Lee el archivo y hoja del libro correspondiente
my_sheet = "query (82)"
file_name = "prueba_datos.xlsx"
data = read_excel(file_name, sheet_name=my_sheet)

# Crea un duplicado
new_data = data.copy()

# Cogemos los nombres que nos interesan para la posterior insercion
new_data = new_data[['Nombre', 'Titulación', 'Facultad', 'Universidad de Destino', 'Periodo', 'Idioma', 'Estancia' , 'Plaza concedida']]

# Incorporamos las columnas que encesitaremos para poder realizar correctamente la isnercion en SQL
new_data.insert(1, 'Apellidos', "-")
new_data.insert(7, 'Cuatri', 0)
new_data.insert(10, 'Plazas_1', 1)
new_data.insert(11, 'Plazas_2', 2)

# Aplicamos el filtro quedandonos solamente con los procesos de movilidad de la EPS que es para quien esta dirigido el proyecto
new_data = new_data[(new_data.Facultad=="EPS")]

rows = new_data.shape[0]


#print(names_surnames["nombre"][1] + names_surnames["apellidos"][1])


# 8. Exportamos a archivo excel nuevo con la informacion ya filtrada y ordenada
new_data.to_excel(r'nuevo4.xlsx', index = False)



import xlsxwriter
 
libro = xlsxwriter.Workbook('nuevo4.xlsx')
hoja = libro.add_worksheet()

names_surnames = {
    "nombre": ["Nacho", "Paloma", "Rosa", "Lucas", "Enrique", "Pablo", "Mireia", "Patricia", "Laura", "Mario", "Esteban", "Francisco", "Javier", "Alejandro", "Diego", "Iván", "Jaime", "Jesús", "Sonia","Santiago", "Felipe", "Eugenia", "Ana", "Adrián", "Álvaro", "Ricardo", "Sofía", "María", "Paula", "Mauro", "Alberto", "David", "Sergio", "José", "Samuel", "Manuel", "Marta", "Claudia", "Alejandra", "Julia", "Alba", "Jorge", "Víctor", "Emma", "Nuria", "Lucía", "Encarnación"],
    "apellidos": ["Prieto Meloso", "Esteban Fernández", "Menéndez Pelayo", "Engracia Tomás", "Encinas Sabater", "Pastor Morales", "Escobar Alonso", "Legarda García", "Rivera Montero", "Trujillo del Viso", "Granado Fernández", "Martínez Pelayo", "Huarte González", "Colmenarejo Ten", "Álvarerz Gallardo", "Del Río García", "Mata Gazulla", "Herrero Lalana", "Carrasco Tellez", "Migallón Gallardo", "Romero Borobio", "Elías Fernández", "Roldan García", "Vizoso Pardo", "García Antolín", "Sanchidrián Prieto", "Fernandez Palomo", "Pérez Sánchez", "Pradales Catalina", "Piñero ALquegui", 
    "Coronado Galdos", "Pelayo Prieto", "Fernández Tomás", "García Alonso", "Montero Bargueño", "Ortiz Mayor", "Bernal Romanillos", "Ortega Vidal", "Bremond García", "Cabanas Romero", "Iglesias Gandarias", "Zaballos Fernández", "Sierra Mendía", "García Antolín", "Fernández Torronteras", "Muñoz Granado", "Cole de Prada" ] }


rows=47
for i in range(rows):
    for j in range(2):
        print(hoja.write(i,j,names_surnames["nombre"][i]))
        hoja.write(i,j,names_surnames["apellidos"][i])

print(hoja)


'''

'''