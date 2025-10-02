from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt





app = Flask(__name__)
app.config['SECRET_KEY'] = 'fb9cf91dc75ad7e4a499d552d3f28b4f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from blogapi import routes