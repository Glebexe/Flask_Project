from . import db

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

class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))


