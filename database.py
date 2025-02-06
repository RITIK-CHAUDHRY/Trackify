from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client['Trackify']

class Database:
    @staticmethod
    def store_user(username, email, password):
        users = db.users
        hashed_password = generate_password_hash(password)
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "created_at": datetime.utcnow(),
            "settings": {
                "currency": "INR",
                "notifications": True,
                "budget_alerts": True,
                "theme": "light"
            },
            "profile": {
                "phone": "",
                "avatar": "",
                "preferences": {
                    "language": "en",
                    "email_notifications": True
                }
            }
        }
        users.insert_one(user_data)

    @staticmethod
    def verify_user(email, password):
        users = db.users
        user = users.find_one({"email": email})
        if user and check_password_hash(user['password'], password):
            return True
        return False

    @staticmethod
    def get_user_by_email(email):
        users = db.users
        return users.find_one({"email": email})

    @staticmethod
    def add_expense(user_email, amount, category, date, payment_method, notes=None):
        expenses = db.expenses
        expense_data = {
            "user_email": user_email,
            "amount": float(amount),
            "category": category,
            "date": datetime.strptime(date, '%Y-%m-%d'),
            "payment_method": payment_method,
            "notes": notes,
            "created_at": datetime.utcnow()
        }
        expenses.insert_one(expense_data)

    @staticmethod
    def get_user_expenses(user_email, start_date=None, end_date=None):
        expenses = db.expenses
        query = {"user_email": user_email}
        
        if start_date and end_date:
            query["date"] = {
                "$gte": datetime.strptime(start_date, '%Y-%m-%d'),
                "$lte": datetime.strptime(end_date, '%Y-%m-%d')
            }
            
        return list(expenses.find(query).sort("date", -1))