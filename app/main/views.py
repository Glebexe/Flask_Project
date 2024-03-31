# from app.main.forms import SimpleForm
from flask import abort, render_template, redirect, url_for
from flask_mail import Message
from app.models import *
from app import db
from . import main
from .. import mail



@main.route("/")
def index():
    objs = Job.query.all()
    jobs = []
    for job in objs:
        jobs.append({'job_name': job.job_name, 'location': job.location, 'website': job.website})
    return render_template("index.html", jobs=jobs)


@main.route("/hi/<name>")
def hello_user(name):
    return '<body style="font-family: Arial, sans-serif; background-color: #f0f0f0; text-align: center;">' \
           ' <h1 style="color: #333;">Welcome to My Flask Page!</h1>' \
           '<p style="color: #666;">Hello, <span style="font-weight: bold;">{}</span>!</p></body>'.format(name)

@main.route("/ops")
def ops():
    return abort(400)



@main.route('/send_email')
def email():
    send_mail('ihtiornis2020@gmail.com', 'My email sent from Flask app', 'mail_text')
    return redirect(url_for('index'))

def send_mail(to, subject, template, **kwargs):
    msg = Message(subject,
                  sender=main.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.body = render_template(template+'.txt', **kwargs)
    # msg.html = render_template(template+'.html', **kwargs)
    mail.send(msg)

@main.route('/form', methods=['GET','POST'])
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

