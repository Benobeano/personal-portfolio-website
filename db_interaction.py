# File for interacting with db directly, add entities, view tables, popultate tables or whatever

from app import create_app
from app.extensions import db
from app.models import Project, Skill, Experience, Image, Link, ContactMessage, User, Portfolio
from app.repositories.repository import Repository

# Create the Flask app instance
app = create_app()
repo = Repository()


def create_user(first_name, last_name, username, password_hash):
    """Add a new user to the database."""
    with app.app_context():
        new_user = User(first_name=first_name, last_name=last_name, username=username, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        print(f"User '{username}' created successfully!")

def add_new_user_with_repository(first_name, last_name, username, password):
    try:
        new_user = repo.create_user(first_name=first_name, last_name=last_name, username=username, password=password)
        print(f"User '{new_user.username}' created successfully!")
    except ValueError as e:
        print(str(e))

def list_users():
    """Query all users from the database."""
    with app.app_context():
        users = User.query.all()
        for user in users:
            print(f"ID: {user.id}, Name: {user.first_name} {user.last_name}, Username: {user.username}")

if __name__ == '__main__':
    with app.app_context():
        # run methods here
        list_users()
