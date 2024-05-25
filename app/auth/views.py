from app import mail
from threading import Thread
from flask_mail import Message
from flask import render_template, redirect, request, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User


@auth.before_app_request
def before_request():
    """
    :return: auth.unconfirmed page if user is unauthorized
    """
    if current_user.is_authenticated and not current_user.confirmed and request.blueprint != 'auth'\
       and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login data processing
    :return: login form
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_verify(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get("next")
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password')
    return render_template("auth/login.html", form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registration data processing
    :return: registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_confirm(user, token)
        return redirect(url_for('auth.login'))
    return render_template("auth/registration.html",form=form)


@auth.route('/logout')
@login_required
def logout():
    """
    Logout user
    :return: main page
    """
    logout_user()
    flash('You are logout')
    return redirect(url_for('main.index'))


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    """
    Registration confirmation
    :param token: unique generated confirmation token
    :return: main page
    """
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token[2:]):
        db.session.commit()
        flash("Ваше подтверждение прошло успешно, спасибо!")
    else:
        flash("Ваша ссылка не валидна или истекла")
    return redirect(url_for('main.index'))


@auth.route("/unconfirmed")
def unconfirmed():
    """
    :return: unconfirmed page if user unconfirmed, else main page
    """
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


def send_confirm(user, token):
    """
    Form data for mail send
    :param user:
    :param token: unique generated confirmation token
    :return: main page
    """
    send_mail(user.email, 'Confirm your account', 'auth/confirm', user=user, token=token)
    redirect(url_for('main.index'))


def send_mail(to, subject, template, **kwargs):
    """
    Send mail to user for confirmation account
    :param to: recipient
    :param subject: mail subject
    :param template: mail template
    :param kwargs:
    :return: thread of mail send
    """
    msg = Message(subject,
                  sender='glebbedakov@gmail.com',
                  recipients=[to])
    try:
        msg.html = render_template(template+'.html', **kwargs)
    except:
        msg.body = render_template(template+'.txt', **kwargs)
    from app_file import flask_app
    thread = Thread(target=send_async_email, args=[flask_app, msg])
    thread.start()
    return thread


def send_async_email(app, msg):
    """
    Asynchronously send email
    :param app:
    :param msg: email message
    :return:
    """
    with app.app_context():
        mail.send(msg)
