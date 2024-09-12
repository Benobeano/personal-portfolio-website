from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Instantiate the db in extensions so it can be accessed outside of application context. 
db = SQLAlchemy()
bcrypt = Bcrypt()
