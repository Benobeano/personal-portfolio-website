import os

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'app/db/portfolioDatabase.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False