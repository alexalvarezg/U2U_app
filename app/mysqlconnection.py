import webbrowser
import mysql.connector


conn = mysql.connector.connect(user='root', password='TFG_Alexa1!',
                              host='localhost',database='tfg')

if conn:
    print ("Connected Successfully")
else:
    print ("Connection Not Established")

select_employee = """SELECT * FROM estudiantes"""
cursor = conn.cursor()
cursor.execute(select_employee)
result = cursor.fetchall()

p = []

tbl = "IDNameEmailPhone"
p.append(tbl)

for row in result:
    a = "%s"%row[0]
    p.append(a)
    b = "%s"%row[1]
    p.append(b)
    c = "%s"%row[2]
    p.append(c)
    d = "%s"%row[3]
    p.append(d)