from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from extensions import db
# db = SQLAlchemy()

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
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    images = db.relationship('Image', backref='project', lazy=True, cascade="all, delete-orphan")
    links = db.relationship('Link', backref='project', lazy=True, cascade="all, delete-orphan")
    
    # Many-to-many relationship with Skill via project_skill_association
    skills = db.relationship('Skill', secondary=project_skill_association, backref=db.backref('projects', lazy=True))

class Skill(db.Model):
    __tablename__ = 'skill'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(255), nullable=True)
    display_order = db.Column(db.Integer, nullable=True)
    
    # Many-to-many relationship with Project via project_skill_association
    # Many-to-many relationship with Experience via experience_skill_association
    experiences = db.relationship('Experience', secondary=experience_skill_association, backref=db.backref('skills', lazy=True))

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
    skills = db.relationship('Skill', secondary=experience_skill_association, backref='experiences')

class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    # Store the binary data of the image
    data = db.Column(db.LargeBinary, nullable=False)
    alt_text = db.Column(db.String(255), nullable=True) #optional

    # Foreign keys to reference Project and Experience tables
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    experience_id = db.Column(db.Integer, db.ForeignKey('experience.id'), nullable=True)

    # Relationships with Project and Experience
    project = db.relationship('Project', backref='images', lazy=True)
    experience = db.relationship('Experience', backref='images', lazy=True)


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
    email = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
