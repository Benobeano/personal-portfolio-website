from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from models import 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolioDatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def home():
    return "Portfolio App!"

if __name__ == '__main__':
    app.run(debug=True)