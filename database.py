from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

client = MongoClient("mongodb://localhost:27017/Trackify")
db = client['Trackify']
users_collection = db['users']

def store_user(username, email, password):
    hashed_password = generate_password_hash(password)  # Hash the password before storing
    users_collection.insert_one({"username": username, "email": email, "password": hashed_password})

def verify_user(email, password):
    user = users_collection.find_one({"email": email})
    if user and check_password_hash(user['password'], password):  # Check hashed password
        return True
    return False
