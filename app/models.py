from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from . import login_manager

from authlib.jose import jwt, JsonWebSignature

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200))
    description = db.Column(db.String(2000))
    jobs = db.relationship('Job', backref='Company')

    def __repr__(self):
        return self.company_name
class Job(db.Model):

    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(200))
    description = db.Column(db.String(2000))
    salary = db.Column(db.Integer)
    location = db.Column(db.String(200))
    website = db.Column(db.String(200))
    company = db.Column(db.Integer, db.ForeignKey('companies.id'))

    def __repr__(self):
        return self.job_name

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, index=True)
    email = db.Column(db.String(60), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)

    def generate_confirmation_token(self):
        jws = JsonWebSignature()
        protected = {'alg': 'HS256'}
        payload = self.id
        secret = 'secret'
        return jws.serialize_compact(protected, payload, secret)

    def confirm(self, token):
        jws = JsonWebSignature()
        data = jws.deserialize_compact(s=token, key='secret')
        if data.payload.decode('utf-8') != str(self.id):
            print("It's not your token")
            return False
        else:
            self.confirmed = True
            db.session.add(self)
            return True

    @property
    def password(self):
        raise AttributeError('password not enable for read')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, "pbkdf2")

    def password_verify(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))