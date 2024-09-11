from flask_sqlalchemy import SQLAlchemy

# Instantiate the db in tetensions so it can be accessed outside of application context. 
db = SQLAlchemy()
