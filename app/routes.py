# from flask import render_template
# from . import db
from app.models import User, Portfolio, Project
from app.extensions import db
from flask import abort, redirect, render_template, request, url_for
from app.forms import MessageForm
from app.repository import Repository



repo = Repository()

def register_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def home():
        portfolios = Portfolio.query.all()
        form = MessageForm()
        
        if form.validate_on_submit():
            # Handle message submission
            message = repo.add_message(
                name=form.name.data,
                email=form.email.data,
                sent_to=form.sent_to.data,
                message=form.message.data
            )
            db.session.add(message)
            db.session.commit()
            flash('Message sent successfully!')
            return redirect(url_for('home'))
        
        return render_template('home.html', portfolios=portfolios, form=form)

    


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

    

