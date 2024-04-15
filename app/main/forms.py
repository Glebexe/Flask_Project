from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from app.models import Company


class JobForm(FlaskForm):
    job_name = StringField("Работа:", validators=[DataRequired()])
    description = StringField("Описание:", validators=[DataRequired()])
    salary = IntegerField("Зарплата:", validators=[DataRequired()])
    location = StringField("Место:", validators=[DataRequired()])
    website = StringField("Сайт:", validators=[DataRequired()])

    companies = Company.query.all()
    company = SelectField("Компания", choices=companies)

    submit = SubmitField("Отправить")

class Sign_up_in_Form(FlaskForm):
    username = StringField("Введите имя пользователя")
    password = PasswordField("Введите пароль")

    submit = SubmitField("Отправить")