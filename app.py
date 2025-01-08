# Finance App

from flask import Flask, render_template, request, redirect, url_for, flash
from database import register_user, check_user  # Import the register_user and check_user functions
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)

# Configure Google OAuth
google_bp = make_google_blueprint(client_id='YOUR_GOOGLE_CLIENT_ID', client_secret='YOUR_GOOGLE_CLIENT_SECRET', redirect_to='auth_google')
app.register_blueprint(google_bp, url_prefix='/google_login')

@app.route('/')
def index():
    return render_template('landing_page.html')  # Set landing page as the default

@app.route('/landing')
def landing():
    return render_template('landing_page.html')

@app.route('/auth', methods=['GET'])
def auth():
    return render_template('auth.html')
    
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    # Add authentication logic here
    flash('Logged in successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/auth/google')
def auth_google():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/plus/v1/people/me')
    assert resp.ok, resp.text
    # Process user information and store in the database
    return redirect(url_for('index'))

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')  # Create this template later

@app.route('/guest')
def guest():
    # Logic for continuing as a guest
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
