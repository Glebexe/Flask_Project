import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

basedir = os.path.abspath(os.path.dirname(__file__))
flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = 'my secret key'
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flask_project_bd'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

flask_app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
flask_app.config['MAIL_PORT'] = 587
flask_app.config['MAIL_USE_TLS'] = True
flask_app.config['MAIL_USERNAME'] = 'glebbedakov@gmail.com'
flask_app.config['MAIL_PASSWORD'] = 'zgdf kuwy mukt awph'


bootstrap = Bootstrap(flask_app)
db = SQLAlchemy(flask_app)
mail = Mail(flask_app)

from models import *
migrate = Migrate(flask_app, db)

from app import routes
