# File for interacting with db directly, add entities, view tables, popultate tables or whatever

from datetime import datetime
from app import create_app
from app.extensions import db
from app.models import Project, Skill, Experience, Image, Link, ContactMessage, User, Portfolio
from app.repository import Repository

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

def create_user_with_portfolio(first_name, last_name, username, password_hash):
    """Create a user with a full portfolio, including projects, skills, and experiences."""
    with app.app_context():
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"Username '{username}' already exists. Please choose a different username.")
            return

        # Step 1: Create the User
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password_hash=password_hash
        )
        db.session.add(user)
        db.session.commit()  # Save user to get the ID for the portfolio

        # Step 2: Create the Portfolio
        portfolio = Portfolio(
            title=f"{first_name}'s Portfolio",
            description=f"A portfolio for {first_name} {last_name}.",
            user_id=user.id
        )
        db.session.add(portfolio)
        db.session.commit()  # Save portfolio to get the ID for related entities

        # Step 3: Create Skills
        skill1 = Skill(name="Python", description="Python programming language", portfolio_id=portfolio.id)
        skill2 = Skill(name="Flask", description="Flask web framework", portfolio_id=portfolio.id)
        db.session.add_all([skill1, skill2])
        db.session.commit()

        # Step 4: Create Projects
        project1 = Project(
            title="Personal Website",
            description="A personal website built using Flask and HTML/CSS.",
            portfolio_id=portfolio.id
        )
        project1.skills.append(skill1)  # Link skill1 to project1
        project1.skills.append(skill2)  # Link skill2 to project1
        db.session.add(project1)
        db.session.commit()

        # Step 5: Create Experiences
        experience1 = Experience(
            title="Software Developer",
            organization="Tech Company",
            location="Remote",
            description="Worked on various web development projects.",
            start_date=datetime(2021, 1, 1),
            end_date=datetime(2022, 12, 31),
            portfolio_id=portfolio.id
        )
        experience1.skills.append(skill1)  # Link skill1 to experience1
        db.session.add(experience1)
        db.session.commit()

        # Step 6: Add Images and Links to Project
        image1 = Image(image_data=b'sampleimagedata',  # Replace with actual binary data for the image
            alt_text="Screenshot of the personal website",
            project_id=project1.id
        )
        link1 = Link(
            url="https://personalwebsite.com",
            description="Live site",
            project_id=project1.id
        )
        db.session.add_all([image1, link1])
        db.session.commit()

        print(f"User '{username}' with a complete portfolio created successfully!")

def show_all_tables_and_contents():
    """Show all tables and their contents."""
    with app.app_context():
        # Get all table names in the database
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()

        for table_name in tables:
            print(f"\nTable: {table_name}")

            # Reflect the table dynamically and query all its rows
            if table_name in db.metadata.tables:
                table = db.metadata.tables[table_name]
            else:
                table = db.Table(table_name, db.metadata, autoload_with=db.engine)

            # Query all rows in the table
            rows = db.session.execute(table.select()).fetchall()

            # Get column names from the table
            columns = table.columns.keys()

            # Display the rows
            if rows:
                for row in rows:
                    # Use the column names to map row data to a dictionary
                    row_dict = {column: getattr(row, column) for column in columns}
                    print(row_dict)
            else:
                print("No data available in this table.")

if __name__ == '__main__':
    with app.app_context():
        # run methods here
        # table_names = db.inspect(db.engine).get_table_names()
        # print("Tables in the database:", table_names)
        # create_user_with_portfolio(
        #     first_name="John",
        #     last_name="Doe",
        #     username="johndoe3",
        #     password_hash="hashed_password_here"  # Replace with an actual hashed password
        # )
        # list_users()
        show_all_tables_and_contents()