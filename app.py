from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import Database
from expense_analyzer import ExpenseAnalyzer
from ai_helper import analyze_spending_patterns, get_budget_recommendations, get_chatbot_response
from config import Config
from datetime import datetime
import requests
import json

app = Flask(__name__)
app.config.from_object(Config)
db = Database()

@app.route("/")
def home():
    if 'email' in session:
        return redirect(url_for('main_home'))
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
        try:
            db.store_user(username, email, password)
            return redirect(url_for('home'))
        except Exception as e:
            return str(e), 400
    return "Passwords do not match", 400

@app.route("/login", methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']
    if db.verify_user(email, password):
        session['email'] = email
        return redirect(url_for('main_home'))
    return "Invalid credentials", 401

@app.route("/main_home")
def main_home():
    if 'email' not in session:
        return redirect(url_for('home'))
    user = db.get_user_by_email(session['email'])
    return render_template("main_home.html", username=user['username'])

@app.route("/dashboard")
def dashboard():
    if 'email' not in session:
        return redirect(url_for('home'))
    
    user_email = session['email']
    expenses = db.get_user_expenses(user_email)
    user = db.get_user_by_email(user_email)
    
    analyzer = ExpenseAnalyzer(expenses)
    monthly_summary = analyzer.get_monthly_summary()
    category_breakdown = analyzer.get_category_breakdown()
    trend_graph = analyzer.generate_trend_graph()
    alerts = analyzer.get_spending_alerts()
    
    ai_insights = analyze_spending_patterns(expenses)
    
    return render_template(
        "dashboard.html",
        username=user['username'],
        monthly_summary=monthly_summary,
        category_breakdown=category_breakdown,
        trend_graph=trend_graph,
        alerts=alerts,
        ai_insights=ai_insights
    )

@app.route("/news")
def news():
    if 'email' not in session:
        return redirect(url_for('home'))
    
    try:
        # Using Alpha Vantage API for financial news
        api_key = Config.ALPHA_VANTAGE_API_KEY
        url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={api_key}&topics=finance"
        response = requests.get(url)
        news_data = response.json().get('feed', [])[:10]  # Get latest 10 news items
        return render_template("news.html", news=news_data)
    except Exception as e:
        return render_template("news.html", news=[], error="Unable to fetch news")

@app.route("/courses")
def courses():
    if 'email' not in session:
        return redirect(url_for('home'))
    return render_template("courses.html")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    if 'email' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    try:
        data = request.get_json()
        user_message = data['message']
        response = get_chatbot_response(user_message)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/add_expense", methods=["POST"])
def add_expense():
    if 'email' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    try:
        data = request.get_json()
        db.add_expense(
            user_email=session['email'],
            amount=data['amount'],
            category=data['category'],
            date=data['date'],
            payment_method=data['payment_method'],
            notes=data.get('notes')
        )
        return jsonify({"message": "Expense added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/get_insights", methods=["GET"])
def get_insights():
    if 'email' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    expenses = db.get_user_expenses(session['email'])
    insights = analyze_spending_patterns(expenses)
    return jsonify({"insights": insights})

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)