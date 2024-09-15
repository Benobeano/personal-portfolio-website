from datetime import datetime
from app import create_app
from app.extensions import db
from app.repository import Repository
from app.models import Education, Project, Skill, Experience, Image, Link, ContactMessage, User, Portfolio, Organization

# Create the Flask app instance
app = create_app()

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

def read_image(file_path):
    """Reads an image file and returns its binary data."""
    with open(file_path, 'rb') as file:
        return file.read()
    
def create_user_with_portfolio_and_image(first_name, last_name, username, password_hash, image_path, alt_text=""):
    """Create a user with a full portfolio, including projects, skills, experiences, and a user image."""
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

        # Step 2: Add Image for the User
        if image_path:
            image_data = read_image(image_path)
            user_image = Image(
                image_data=image_data,
                alt_text=alt_text,
                user_id=user.id  # Link the image to the user
            )
            db.session.add(user_image)
            db.session.commit()

        # Step 3: Create the Portfolio
        portfolio = Portfolio(
            title=f"{first_name} {last_name}'s Portfolio",
            description="Software Developer Co-op at UPS and Computer Science Student at Western Kentucky University",
            user_id=user.id
        )
        db.session.add(portfolio)
        db.session.commit()  # Save portfolio to get the ID for related entities

        # Step 4: Create Skills
        skills = [
            "Google Cloud Platform", "Flask", "Angular", "C#/ .NET", "GCP OCR", 
            "Java", "Couchbase", "MySQL", "Kotlin", "Android Studio", 
            "Unity", "Python"
        ]
        skill_objects = [Skill(name=skill, portfolio_id=portfolio.id) for skill in skills]
        db.session.add_all(skill_objects)
        db.session.commit()

        # Step 5: Create Projects
        project1 = Project(
            title="Wildflower Boutique",
            description="A website for shopping clothing, accessories, and footwear developed using PHP, JavaScript, HTML/CSS, and MySQL. It has a user-friendly interface allowing product searches, viewing details, and making purchases.",
            portfolio_id=portfolio.id
        )
        project2 = Project(
            title="Superhero Showdown",
            description="A 2D game developed with Unity and Blender, featuring a superhero controlled by the user, battling through levels with enemy objects. Unity was used for mechanics and Blender for creating 2D models and animations.",
            portfolio_id=portfolio.id
        )
        project3 = Project(
            title="Eat Healthy",
            description="A user-friendly Android app developed with Android Studio and Kotlin for sharing healthy recipes and fostering community connections.",
            portfolio_id=portfolio.id
        )
        # Link relevant skills
        project1.skills.extend(skill_objects[:3])  # Example linking skills; adjust as needed
        db.session.add_all([project1, project2, project3])
        db.session.commit()

        # Step 6: Create Experiences with unique variable names
        experience1 = Experience(
            title="Software Developer Co-Op",
            organization="UPS",
            location="Remote",
            description="Full stack software developer, working with Angular, .NET, and Couchbase.",
            start_date=datetime(2024, 8, 16),
            portfolio_id=portfolio.id
        )
        experience2 = Experience(
            title="Software Developer Intern",
            organization="UPS",
            location="Louisville, KY",
            description="Developed a full-stack application utilizing Google Cloud OCR for data extraction from images and video feeds, aiding shipment tracking.",
            start_date=datetime(2024, 6, 3),
            end_date=datetime(2024, 8, 16),
            portfolio_id=portfolio.id
        )
        experience3 = Experience(
            title="Math Tutor",
            organization="Western Kentucky University",
            location="Bowling Green, KY",
            description="Provide support to college students struggling with math coursework up to Calculus 2.",
            start_date=datetime(2023, 8, 1),
            end_date=datetime(2023, 8, 31),
            portfolio_id=portfolio.id
        )
        experience4 = Experience(
            title="WKU SEAS Ambassador",
            organization="Western Kentucky University",
            location="Bowling Green, KY",
            description="Represent the School of Engineering and Applied Sciences in various outreach activities.",
            start_date=datetime(2024, 5, 1),
            portfolio_id=portfolio.id
        )
        experience5 = Experience(
            title="Computer Science Tutor",
            organization="Western Kentucky University",
            location="Bowling Green, KY",
            description="Provide academic support to computer science students.",
            start_date=datetime(2023, 8, 1),
            end_date=datetime(2024, 8, 1),
            portfolio_id=portfolio.id
        )
        experience1.skills.append(skill_objects[0])  # Link relevant skills
        db.session.add_all([experience1, experience2, experience3, experience4, experience5])
        db.session.commit()

        # Step 7: Add Organizations
        organization1 = Organization(
            title="Treasurer",
            organization="Phi Mu Delta Tau",
            description="Responsible for managing the organization's finances and ensuring its operations run smoothly.",
            portfolio_id=portfolio.id
        )
        organization2 = Organization(
            title="Activity Coordinator",
            organization="Women in Science and Engineering",
            description="Plans and organizes events for a student-led organization dedicated to empowering women in STEM.",
            portfolio_id=portfolio.id
        )
        organization3 = Organization(
            title="Member",
            organization="Order of Omega Gamma Beta",
            description="Greek Honor Society representing the top 5 percent of Greek life at WKU.",
            portfolio_id=portfolio.id
        )
        db.session.add_all([organization1, organization2, organization3])

        # Correct Step: Add Education with the correct portfolio_id
        education = Education(
            school="Western Kentucky University",
            major="Computer Science",
            minor=None,  # If no minor, set as None
            gpa=3.97,
            degreeType="Bachelor of Science",
            graduationYear=2025,
            portfolio_id=portfolio.id  # Correctly link to the portfolio
        )
        db.session.add(education)
        db.session.commit()

        print(f"User '{username}' with a complete portfolio and image created successfully!")

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
        db.create_all()
        create_user_with_portfolio_and_image(
            first_name="Amy",
            last_name="Patel",
            username="ampate01",
            password_hash="amy",  # Replace with an actual hashed password
            image_path="/Users/Development/GitHub/personal-portfolio-website/Images/amysImg.JPEG",  # Provide the correct path to your image
            alt_text="Profile picture of Amy"
        )
