from flask import Flask
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import config

bootstrap = Bootstrap4()
db = SQLAlchemy()
mail = Mail()


def create_app(config_name='default'):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config[config_name])
    config[config_name].init_app(flask_app)

    bootstrap.init_app(flask_app)
    db.init_app(flask_app)
    mail.init_app(flask_app)

    from .main import main as main_bluprint
    flask_app.register_blueprint(main_bluprint)

    return flask_app
