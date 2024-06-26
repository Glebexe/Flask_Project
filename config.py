import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my secret key'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
    MAIL_PORT = os.environ.get('MAIL_PORT') or '587'
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or 5870
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'glebbedakov@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'zgdf kuwy mukt awph'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_ADMIN = 'test@test.ru'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'mysql://root:@localhost/flask_project_bd'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'mysql://root:@localhost/flask_project_bd'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'mysql://root:@localhost/flask_project_bd'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
