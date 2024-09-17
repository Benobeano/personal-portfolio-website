# from flask import render_template
# from . import db
from app.extensions import db
from flask import abort, redirect, render_template, request, send_file, url_for,flash
from app.forms import MessageForm
from app.repository import Repository
from io import BytesIO
from app.models import Education, Image, User, Portfolio, Project, Experience, Skill, Organization

repo = Repository()

def register_routes(app):
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

        return render_template('home.html', portfolio_data=portfolio_data, form=form)

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
    

