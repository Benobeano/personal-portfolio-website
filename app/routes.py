# from flask import render_template
# from . import db
from app.models import User, Portfolio, Project
from flask import abort, redirect, render_template, request, url_for


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
        
        # Fetch the portfolio and its associated projects
        portfolio = user.portfolio
        projects = Project.query.filter_by(portfolio_id=portfolio.id).all()
        
        # Render the portfolio page with the projects
        return render_template('portfolio.html', portfolio=portfolio, projects=projects)

    

