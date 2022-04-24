from distutils.command.config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

'''
The URI connection sintaxis looks like:
    app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user:password!@host:port/database'
'''


app = Flask(__name__, template_folder='../templates/', static_folder='../static')

#esto no me convence del todo

path = "gitignore/config.json"
with open(path, 'r') as f:
    conf = json.load(f)

user = conf['CONFIGURATION']['MYSQL_USER']
port = conf['CONFIGURATION']['PORT']
password = conf['CONFIGURATION']['MYSQL_PASSWORD']
db = conf['CONFIGURATION']['MYSQL_DB']
host = conf['CONFIGURATION']['MYSQL_HOST']
sk = conf['SECRET_KEY']

app.secret_key = sk
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://' + user + ':' + password + '@' + host+':'+ port + '/' +db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)





#views for models antiguo
#from app import views

from app import new_views


#from .views import *