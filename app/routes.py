# from flask import render_template
# from . import db

def register_routes(app):
    @app.route('/')
    def home():
        return "Portfolio Project!"

