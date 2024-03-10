from app import app
from app.forms import SimpleForm
from flask import abort, render_template, redirect, url_for, session


@app.route("/")
def index():
    user_data = {'name': session.get('name','blank'),
                 'surname': session.get('surname','blank'),
                 'email': session.get('email','blank'),
                 'codingExperience': session.get('codingExperience','blank'),
                 'setAvatar': session.get('setAvatar',False)}
    parameters = {"parameter1": "Весь текст написан на английском, а этот на русском",
                  "parameter2": "Вот, я смог повторить отправку параметров из routes в index.html",
                  "userData": user_data}
    return render_template("index.html", parameters=parameters)


@app.route("/hi/<name>")
def hello_user(name):
    return '<body style="font-family: Arial, sans-serif; background-color: #f0f0f0; text-align: center;">' \
           ' <h1 style="color: #333;">Welcome to My Flask Page!</h1>' \
           '<p style="color: #666;">Hello, <span style="font-weight: bold;">{}</span>!</p></body>'.format(name)

@app.route("/ops")
def ops():
    return abort(400)


@app.errorhandler(400)
def error_request(e):
    return render_template("400.html"), 400


@app.route('/form', methods=['GET','POST'])
def test_form():
    form = SimpleForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['surname'] = form.surname.data
        session['email'] = form.email.data
        session['codingExperience'] = form.codingExperience.data
        session['setAvatar'] = form.setAvatar.data
        return redirect(url_for('index'))
    return render_template('formTemplate.html', form=form)
