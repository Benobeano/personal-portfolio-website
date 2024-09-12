# Run this file to create the portfolio database

import os
from app import create_app
from app.extensions import db

# Ensure the directory for the database exists
db_dir = os.path.join(os.path.dirname(__file__), 'app/db')
os.makedirs(db_dir, exist_ok=True)

# Set up the app
app = create_app()

with app.app_context():
    db.create_all()
    print("Database created successfully!")
