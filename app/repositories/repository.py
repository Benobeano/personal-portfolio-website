from app.extensions import db, bcrypt
from app.models import User

class Repository:
    def __init__(self):
        pass

    def create_user(self, first_name, last_name, username, password):
        """Add a new user to the database with a hashed password."""
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            raise ValueError(f"Username '{username}' is already taken.")

        # Hash the password before storing it
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create and save the new user
        new_user = User(first_name=first_name, last_name=last_name, username=username, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return new_user
