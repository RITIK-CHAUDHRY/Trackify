from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/Trackify")
db = client['Trackify']
users_collection = db['users']

def check_users():
    users = users_collection.find()
    for user in users:
        print(user)

if __name__ == "__main__":
    check_users()
