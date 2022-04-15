#from distutils.command.config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy, create_engine
import json
from sqlalchemy.orm import scoped_session, sessionmaker

'''
The URI connection sintaxis looks like:
    app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user:password!@host:port/database'
'''


app = Flask(__name__, template_folder='C:/Users/ASUS/Desktop/TFG_Github/TFG_Alex-1/templates/')

#esto no me convence del todo

path = "C:/Users/ASUS/Desktop/TFG_Github/TFG_Alex-1/gitignore/config.json"
with open(path, 'r') as f:
    conf = json.load(f)

user = conf['CONFIGURATION']['MYSQL_USER']
port = conf['CONFIGURATION']['PORT']
password = conf['CONFIGURATION']['MYSQL_PASSWORD']
db = conf['CONFIGURATION']['MYSQL_DB']
host = conf['CONFIGURATION']['MYSQL_HOST']


app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://' + user + ':' + password + '@' + host+':'+ port + '/' +db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

engine = create_engine('mysql+pymysql://' + user + ':' + password + '@' + host+':'+ port + '/' +db)
db_connection = scoped_session(sessionmaker(bind=engine))


from app import views


#from .views import *