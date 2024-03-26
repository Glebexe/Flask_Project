from app import flask_app
from app.forms import SimpleForm
from flask import abort, render_template, redirect, url_for, session
from flask_mail import Message
from models import *
from . import mail
from app import db


@flask_app.route("/")
def index():
    objs = Job.query.all()
    jobs = []
    for job in objs:
        jobs.append({'job_name': job.job_name, 'location': job.location, 'website': job.website})
    return render_template("index.html", jobs=jobs)


@flask_app.route("/hi/<name>")
def hello_user(name):
    return '<body style="font-family: Arial, sans-serif; background-color: #f0f0f0; text-align: center;">' \
           ' <h1 style="color: #333;">Welcome to My Flask Page!</h1>' \
           '<p style="color: #666;">Hello, <span style="font-weight: bold;">{}</span>!</p></body>'.format(name)

@flask_app.route("/ops")
def ops():
    return abort(400)


@flask_app.errorhandler(400)
def error_request(e):
    return render_template("400.html"), 400

@flask_app.route('/send_email')
def email():
    send_mail('ihtiornis2020@gmail.com', 'My email sent from Flask app', 'mail_text')
    return redirect(url_for('index'))

def send_mail(to, subject, template, **kwargs):
    msg = Message(subject,
                  sender=flask_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.body = render_template(template+'.txt', **kwargs)
    # msg.html = render_template(template+'.html', **kwargs)
    mail.send(msg)

@flask_app.route('/form', methods=['GET','POST'])
def test_form():
    form = SimpleForm()
    if form.validate_on_submit():
        job = Job.query.filter_by(job_name=form.job_name.data).first()
        if not job:
            job = Job()
        job.job_name = form.job_name.data
        job.description = form.description.data
        job.salary = form.salary.data
        job.location = form.location.data
        job.website = form.website.data
        job.company = list(map(str,Company.query.all())).index(form.company.data)+1
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('formTemplate.html', form=form)

