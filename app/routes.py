from app import app
from flask import render_template
from flask import abort


@app.route("/")
def index():
    parameters = {"parameter1": "Весь текст написан на английском, а этот на русском",
                  "parameter2": "Вот, я смог повторить отправку параметров из routes в index.html"}
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
