from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app.extensions import db

# Association table between Project and Skill
project_skill_association = db.Table('project_skill_association',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)

# Association table between Experience and Skill
experience_skill_association = db.Table('experience_skill_association',
    db.Column('experience_id', db.Integer, db.ForeignKey('experience.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)

class Project(db.Model):
    __tablename__ = 'project'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Relationships
    images = db.relationship('Image', backref='project', lazy=True, cascade="all, delete-orphan")
    links = db.relationship('Link', backref='project', lazy=True, cascade="all, delete-orphan")
    
    # Many-to-many relationship with Skill via project_skill_association
    skills = db.relationship('Skill', secondary=project_skill_association, back_populates='projects')

    # Foreign key to Portfolio
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)


class Skill(db.Model):
    __tablename__ = 'skill'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    # Many-to-many relationship with Project (through an association table)
    projects = db.relationship('Project', secondary=project_skill_association, back_populates='skills')

    # Many-to-many relationship with Experience (through an association table)
    experiences = db.relationship('Experience', secondary=experience_skill_association, back_populates='skills')
    
    # Foreign key to Portfolio
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)


class Experience(db.Model):
    __tablename__ = 'experience'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    organization = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)

    # Many-to-many relationship with Skill via experience_skill_association
    skills = db.relationship('Skill', secondary=experience_skill_association, back_populates='experiences')

    # Foreign key to Portfolio
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)


class Organization(db.Model):
    __tablename__ = 'organization'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    organization = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)


class Education(db.Model):
    __tablename__ = 'education'  # Corrected table name
    
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(255), nullable=False)
    major = db.Column(db.String(255), nullable=False)
    minor = db.Column(db.String(255), nullable=True)  # Made minor nullable if it's optional
    gpa = db.Column(db.Float, nullable=False)  # Corrected to Float
    degreeType = db.Column(db.String(255), nullable=False)
    graduationYear = db.Column(db.Integer, nullable=False)

    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)


class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)

    # Store the binary data of the image
    image_data = db.Column(db.LargeBinary, nullable=False)
    alt_text = db.Column(db.String(255), nullable=True)

    # Foreign keys to reference Project, Experience, and User tables
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    experience_id = db.Column(db.Integer, db.ForeignKey('experience.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Field for user association


class Link(db.Model):
    __tablename__ = 'link'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)


class ContactMessage(db.Model):
    __tablename__ = 'contact_message'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    sent_to = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    images = db.relationship('Image', backref='user', lazy=True, cascade="all, delete-orphan")  # Updated backref

    # One-to-one relationship with Portfolio
    portfolio = db.relationship('Portfolio', backref='user', uselist=False, cascade="all, delete-orphan")


class Portfolio(db.Model):
    __tablename__ = 'portfolio'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)  # Title of the portfolio
    description = db.Column(db.Text, nullable=True)     # Optional description
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of creation

    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships with Projects, Experiences, Skills, Organizations, and Education
    projects = db.relationship('Project', backref='portfolio', lazy=True, cascade="all, delete-orphan")
    experiences = db.relationship('Experience', backref='portfolio', lazy=True, cascade="all, delete-orphan")
    skills = db.relationship('Skill', backref='portfolio', lazy=True, cascade="all, delete-orphan")
    organizations = db.relationship('Organization', backref='portfolio', lazy=True, cascade="all, delete-orphan")
    education = db.relationship('Education', backref='portfolio', lazy=True, cascade="all, delete-orphan")
