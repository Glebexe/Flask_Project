from config import config
from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from authlib.integrations.flask_client import OAuth

bootstrap = Bootstrap4()
db = SQLAlchemy()
mail = Mail()
oauth = OAuth()
admin = Admin()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name='default'):

    flask_app = Flask(__name__)
    app_context = flask_app.app_context()
    app_context.push()
    flask_app.config.from_object(config[config_name])
    config[config_name].init_app(flask_app)

    login_manager.init_app(flask_app)
    bootstrap.init_app(flask_app)
    db.init_app(flask_app)
    mail.init_app(flask_app)
    migrate.init_app(flask_app, db)
    oauth.init_app(flask_app)

    from .models import Company, Job, Role, User, UserView, JobView
    admin.init_app(flask_app)
    admin.add_view(ModelView(Company, db.session))
    admin.add_view(JobView(Job, db.session))
    admin.add_view(ModelView(Role, db.session))
    admin.add_view(UserView(User, db.session))

    from .main import main as main_bluprint
    flask_app.register_blueprint(main_bluprint)

    from .auth import auth as auth_blueprint
    flask_app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return flask_app
