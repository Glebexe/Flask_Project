from app import db
from app.models import *
from flask_mail import Message
from flask_login import login_required
from flask import abort, render_template, redirect, url_for, current_app

from . import main
from .forms import *
from .. import mail
from ..decorators import admin_required, permission_required


@main.route("/")
def index():
    """
    The main page with job cards
    :return: main page
    """
    objs = Job.query.all()
    jobs = []
    for job in objs:
        jobs.append({'job_name': job.job_name, 'location': job.location, 'website': job.website})
    return render_template("index.html", jobs=jobs)


@main.route("/hi/<name>")
def hello_user(name):
    """
    Greeting page
    :param name:
    :return: greeting page
    """
    return '<body style="font-family: Arial, sans-serif; background-color: #f0f0f0; text-align: center;">' \
           ' <h1 style="color: #333;">Welcome to My Flask Page!</h1>' \
           '<p style="color: #666;">Hello, <span style="font-weight: bold;">{}</span>!</p></body>'.format(name)


@main.route("/ops")
def ops():
    """
    Test error
    :return: error 400
    """
    return abort(400)


@main.route('/send_email')
def email():
    """
    Send mail to the user
    :return: main page
    """
    send_mail('ihtiornis2020@gmail.com', 'My email sent from Flask app', 'mail_text')
    return redirect(url_for('main.index'))


def send_mail(to, subject, template, **kwargs):
    """
    Forms message to send
    :param to:
    :param subject:
    :param template:
    :param kwargs:
    :return:
    """
    msg = Message(subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.body = render_template(template+'.txt', **kwargs)
    mail.send(msg)


@main.route('/job_form', methods=['GET','POST'])
def job_form():
    """
    Process data from form and add new job
    :return: form for new job
    """
    form = JobForm()
    if form.validate_on_submit():
        job = Job.query.filter_by(job_name=form.job_name.data).first()
        if not job:
            job = Job()
        job.job_name = form.job_name.data
        job.description = form.description.data
        job.salary = form.salary.data
        job.location = form.location.data
        job.website = form.website.data
        arr = []
        for i in Company.query.all():
            arr.append(str(i))
        job.company = arr.index(form.company.data)+1
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('formTemplate.html', form=form)


@main.route('/sign_up_in', methods=['GET','POST'])
def sign_up_in_form():
    """
    User login form
    :return: main page from if data is valid, else form page again
    """
    form = SignUpInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User()
        if user.password != form.password.data:
            user.username = form.username.data
            user.password = form.password.data
            user.role_id = 2
            db.session.add(user)
            db.session.commit()

        return redirect(url_for('main.index'))
    return render_template('formTemplate.html', form=form)


@main.route('/secret')
@login_required
def secret():
    return 'My secret'


@main.route('/admin')
@login_required
@admin_required
def for_admin():
    return "For admin"


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderator():
    return "For moderator"
