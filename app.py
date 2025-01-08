# Finance App

from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['finance_app']
transactions_collection = db['transactions']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        amount = request.form['amount']
        description = request.form['description']
        transactions_collection.insert_one({'amount': amount, 'description': description})
        return redirect(url_for('index'))
    return render_template('add_transaction.html')

@app.route('/view_transactions')
def view_transactions():
    transactions = transactions_collection.find()
    return render_template('view_transactions.html', transactions=transactions)

if __name__ == "__main__":
    app.run(debug=True)
