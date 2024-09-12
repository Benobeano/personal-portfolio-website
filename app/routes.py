# from flask import render_template
# from . import db

from flask import render_template


def register_routes(app):
    @app.route('/')
    def index():
        return render_template('home.html', messages = '')

    

