# Paths & Files
from pathlib import Path# Easier file/folder handling
import bcrypt# Password hashing library
import streamlit as st# import Streamlit for UI and dashboard

DATA_DIR = Path("DATA")  # root-level DATA folder
DATA_DIR.mkdir(parents=True, exist_ok=True)
USERS_FILE = DATA_DIR / "users.txt"
USERS_FILE.touch(exist_ok=True)

# Page Setup
st.set_page_config(page_title="Login / Register", page_icon="🔑", layout="centered")
st.title("🔐 Welcome to the Unified Intelligence Platform")

# Session State
if "logged_in" not in st.session_state:# Track whether user is logged in
    st.session_state.logged_in = False
if "username" not in st.session_state:# Track current username
    st.session_state.username = ""

# Helper Functions
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def load_users():
    users = {}
    for line in USERS_FILE.read_text().splitlines():
        if line.strip():
            u, h = line.strip().split(",", 1)
            users[u] = h
    return users

def save_user(username: str, password: str):
    hashed = hash_password(password)
    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{hashed}\n")

# Redirect if already logged in
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}**.")
    if st.button("Go to Cybersecurity Dashboard"):
        st.switch_page("pages/1_Dashboard.py")  # Redirect to dashboard
    st.stop()# Stop further execution

# Tabs: Login / Register
tab_login, tab_register = st.tabs(["Login", "Register"])

# LOGIN
with tab_login:
    st.subheader("Login")
    login_username = st.text_input("Username", key="login_username")#Input username
    login_password = st.text_input("Password", type="password", key="login_password")#Input password

    if st.button("Log in"):#Login button
        users = load_users()#Load stored users
        #Check credentials
        if login_username in users and verify_password(login_password, users[login_username]):
            st.session_state.logged_in = True#Mark user as logged in
            st.session_state.username = login_username
            st.success(f"Welcome back, {login_username}! 🎉")
            st.switch_page("pages/1_Dashboard.py")  # Redirect to dashboard
        else:
            st.error("Invalid username or password.")#Show error

# REGISTER
with tab_register:
    st.subheader("Register")
    new_username = st.text_input("Choose a username", key="register_username")#Username input
    new_password = st.text_input("Choose a password", type="password", key="register_password")#Password input
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")#Confirm password

    if st.button("Create account"):#Registration button
        users = load_users()#Load existing users
        #Validate input
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")#Empty fields warning
        elif new_password != confirm_password:
            st.error("Passwords do not match.")#Password mismatch
        elif new_username in users:
            st.error("Username already exists. Choose another one.")#Username already exists
        else:
            save_user(new_username, new_password)#Save new user
            st.success("Account created! You can now log in from the Login tab.")
            st.info("Tip: go to the Login tab and sign in with your new account.")
