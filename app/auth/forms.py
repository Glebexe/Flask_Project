from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, ValidationError


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Log in")


def validate_email(field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError("Email already registered")


def validate_username(field):
    if User.query.filter_by(username=field.data).first():
        raise ValidationError('Username is already used')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Username must have only letters, number, dots and underscore'
                                                          )])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2',
                                                                             message="Password doesn't much")])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')
