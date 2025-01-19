# Simulated database for demonstration purposes
users_db = {}

def check_credentials(email, password):
    """Check if the provided credentials match any user in the database."""
    return users_db.get(email) == password

def create_user(email, password):
    """Create a new user in the database."""
    if email in users_db:
        return False  # User already exists
    users_db[email] = password
    return True
