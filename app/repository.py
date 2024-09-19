from app.extensions import db, bcrypt
from app.models import User, ContactMessage

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

    def add_message(self, *, name, email, message, sent_to):
        """Adds a new message to the database."""
        new_message = ContactMessage(
            name=name,
            email=email,
            message=message,
            sent_to=sent_to
        )
        db.session.add(new_message)
        db.session.commit()
        return new_message

    def get_all_messages():
        """Fetches all messages from the database."""
        return ContactMessage.query.all()

    def get_messages_by_portfolio(portfolio_id):
        """Fetches all messages sent to a specific portfolio."""
        return ContactMessage.query.filter_by(sent_to=portfolio_id).all()

    def get_all_messages(self):
        """Fetch all contact messages."""
        return ContactMessage.query.all()


