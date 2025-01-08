from pymongo import MongoClient

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/Trackify')
db = client['finance_app']
transactions_collection = db['transactions']

def check_user(email, password):
    # Check if the user exists in the database
    user = transactions_collection.find_one({'email': email, 'password': password})
    return user is not None

def register_user(email, password):
    try:
        transactions_collection.insert_one({'email': email, 'password': password})  # Storing user data
        return True
    except Exception as e:
        print(f"Error creating account: {e}")
        return False
