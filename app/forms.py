from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class SimpleForm(FlaskForm):
    name = StringField("Имя:", validators=[DataRequired()])
    surname = StringField("Фамилия:", validators=[DataRequired()])
    email = EmailField("Почта", validators=[DataRequired()])
    codingExperience = SelectField("Стаж в IT",
                                   choices=['Никогда не работал', 'Меньше года', 'От 1 до 5 лет', 'Более 5 лет'])
    setAvatar = BooleanField()

    submit = SubmitField("Отправить")
