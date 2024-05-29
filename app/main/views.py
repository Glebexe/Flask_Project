from app import db
from app.models import *
from flask import render_template, redirect, url_for

from . import main
from .forms import *


@main.route("/")
def index():
    """
    The main page with job cards
    :return: main page
    """
    objs = Job.query.all()
    jobs = []
    for job in objs:
        jobs.append({'id': job.id, 'job_name': job.job_name, 'location': job.location, 'website': job.website})
    return render_template("index.html", jobs=jobs)

@main.route('/job/<id>')
def job(id):
    job = Job.query.filter_by(id=id).first()
    return render_template("job.html", job=job)


@main.route('/job_form', methods=['GET', 'POST'])
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
        job.company_id = arr.index(form.company.data)+1
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('formTemplate.html', form=form)
