from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from os import getenv

user = getenv("FF_USER")
password = getenv("FF_PASSWORD")
host = getenv("FF_HOST")
database = getenv("FF_DB")

app = Flask(__name__)

app.config["SECRET_KEY"] = getenv("FF_SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = ("mysql+pymysql://"+user+":"+password+"@"+host+"/"+database)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from application import routes

