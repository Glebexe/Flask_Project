from flask import render_template
from . import main


@main.errorhandler(400)
def error_request(e):
    return render_template("400.html"), 400
