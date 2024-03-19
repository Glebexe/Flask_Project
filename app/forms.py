from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from models import Company
from app import flask_app

class SimpleForm(FlaskForm):
    job_name = StringField("Работа:", validators=[DataRequired()])
    description = StringField("Описание:", validators=[DataRequired()])
    salary = IntegerField("Зарплата:", validators=[DataRequired()])
    location = StringField("Место:", validators=[DataRequired()])
    website = StringField("Сайт:", validators=[DataRequired()])
    with flask_app.app_context():
        companies = Company.query.all()
    company = SelectField("Компания", choices=companies)

    submit = SubmitField("Отправить")
