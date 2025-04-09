import os
from flask import Flask, request, redirect, url_for, flash, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure secret key and database URI (from environment variables in Render production)
app.secret_key = os.environ.get('SECRET_KEY', 'change-me')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://sumoai_db_user:n4grzA6Qp3H9Rvo4VSFBHhRqmhuXWqsm@dpg-cuqb76i3esus738mf0ug-a/sumoai_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

# Define model to store email signups
class EmailSignup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<EmailSignup {self.email}>'

# Create the database tables (only needed once)
@app.before_first_request
def create_tables():
    db.create_all()

# Render the landing page (assuming your HTML is served by a template)
@app.route('/')
def index():
    return render_template('landing_page.html')  # Place your landing page content in templates/index.html

# Endpoint to handle the form submission via POST
@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    if not email:
        flash("Please enter your email.", "error")
        return redirect(url_for('index'))
        
    # Optional: Check if the email already exists
    if EmailSignup.query.filter_by(email=email).first():
        flash("This email is already signed up.", "info")
        return redirect(url_for('index'))
    
    # Create new email record and save to the database
    new_signup = EmailSignup(email=email)
    db.session.add(new_signup)
    db.session.commit()
    
    flash("Thanks for signing up! You're on the early access list.", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
