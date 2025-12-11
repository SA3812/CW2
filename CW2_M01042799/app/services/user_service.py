# app/services/user_service.py
from app.data.users import get_user_by_username, insert_user
import bcrypt

# Register a new user (store username + hashed password)
def register_user(username, password, role="user"):
    # Convert the password to bytes, hash it using bcrypt, then decode to string
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    # Save the new user (username + hashed password) into the database
    insert_user(username, hashed, role)
    # Return success message to the interface
    return True, "User registered."

# Validate login (check username + password)
def login_user(username, password):
    # Get user record from the database
    user = get_user_by_username(username)
    # If username does not exist in the database
    if not user:
        return False, "User not found."

    # Extract the saved (hashed) password
    stored_hash = user["password_hash"]
    # bcrypt.checkpw() compares plain password with saved hash
    if bcrypt.checkpw(password.encode(), stored_hash.encode()):
        return True, "Login successful."
    return False, "Incorrect password."

