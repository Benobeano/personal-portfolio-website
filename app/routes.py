from io import BytesIO
from flask import abort, redirect, render_template, request, send_file, url_for
from app.models import Education, Image, User, Portfolio, Project, Experience, Skill, Organization

def register_routes(app):
    @app.route('/')
    def home():
        # Fetch all users to display on the home page
        users = User.query.all()
        return render_template('home.html', users=users)

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
    

