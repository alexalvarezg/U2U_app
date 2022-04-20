from distutils.command.config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

'''
The URI connection sintaxis looks like:
    app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user:password!@host:port/database'
'''


app = Flask(__name__, template_folder='../templates/')

#esto no me convence del todo

path = "gitignore/config.json"
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

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint #from .main
app.register_blueprint(main_blueprint)

from app import views


#from .views import *