from flask_sqlalchemy import SQLAlchemy

# Instantiate the db in extensions so it can be accessed outside of application context. 
db = SQLAlchemy()
