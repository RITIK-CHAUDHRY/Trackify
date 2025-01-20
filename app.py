from flask import Flask, render_template, request, redirect, url_for, session
from database import store_user, verify_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password == confirm_password:
        store_user(username, email, password)
        return redirect(url_for('home'))  # Redirect to login page
    else:
        return "Passwords do not match", 400

@app.route("/login", methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']
    if verify_user(email, password):
        session['email'] = email
        return redirect(url_for('dashboard'))
    else:
        return "Invalid credentials", 401

@app.route("/dashboard")
def dashboard():
    if 'email' in session:
        return render_template("dashboard.html")
    return redirect(url_for('home'))

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
