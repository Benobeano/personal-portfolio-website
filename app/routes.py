# from flask import render_template
# from . import db
from flask import abort, redirect, render_template, request, send_file, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.extensions import db, login_manager,bcrypt
from app.models import User, Portfolio, Project, Experience, Skill, Organization, Image, Education
from app.forms import MessageForm, SignUpForm, LoginForm
from app.repository import Repository
from io import BytesIO

repo = Repository()

@login_manager.user_loader
def load_user(user_id):
    """Load the user from the database by user ID."""
    return User.query.get(int(user_id))

def register_routes(app):
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        
        form = SignUpForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                password_hash=hashed_password,
                role='user'  # Default role is 'user'
            )
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))

        return render_template('signup.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash('Logged in successfully!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login failed. Please check your username and password.', 'danger')

        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('home'))


    @app.route('/', methods=['GET', 'POST'])
    def home():
        portfolios = Portfolio.query.all()
        form = MessageForm()

        portfolio_data = []
        for portfolio in portfolios:
            user = portfolio.user
            user_image = user.images[0] if user.images else None
            portfolio_data.append({
                'portfolio': portfolio,
                'user_image': user_image
            })

        # If the user is authenticated and is an admin, fetch contact messages
        contact_messages = []
        if current_user.is_authenticated and current_user.role == 'admin':
            contact_messages = repo.get_all_messages()
        
        # Handle message form submission for all users (guests included)
        if form.validate_on_submit():
            # Handle message submission and commit to the database
            repo.add_message(
                name=form.name.data,
                email=form.email.data,
                sent_to=form.sent_to.data,
                message=form.message.data
            )
            flash('Message sent successfully!', 'success')
            return redirect(url_for('home'))

        return render_template('home.html', portfolio_data=portfolio_data, form=form, contact_messages=contact_messages)









    @app.route('/portfolio')
    def show_portfolio():
        # Get the username from the query parameter
        username = request.args.get('username')
        if not username:
            # Redirect to home if no username is provided
            return redirect(url_for('home'))

        # Query the user and their portfolio based on the username
        user = User.query.filter_by(username=username).first()
        if not user or not user.portfolio:
            abort(404, description="Portfolio not found.")
        
        # Fetch the portfolio and its associated projects, experiences, skills, and organizations
        portfolio = user.portfolio
        projects = Project.query.filter_by(portfolio_id=portfolio.id).all()
        experience = Experience.query.filter_by(portfolio_id=portfolio.id).all()
        skill = Skill.query.filter_by(portfolio_id=portfolio.id).all()
        organization = Organization.query.filter_by(portfolio_id=portfolio.id).all()
        images = user.images 
        education = Education.query.filter_by(portfolio_id=portfolio.id).all()
        
        # Render the portfolio page with the projects, experiences, skills, and organizations
        return render_template('portfolio.html', portfolio=portfolio, projects=projects, experience=experience, skill=skill, organization=organization, images=images, education=education)
    
    @app.route('/image/<int:image_id>')
    def get_image(image_id):
        """Serve an image by ID."""
        image = Image.query.get(image_id)
        if not image:
            abort(404, description="Image not found.")
        
        # Use send_file to send the image data
        return send_file(BytesIO(image.image_data), mimetype='image/jpeg')
    

