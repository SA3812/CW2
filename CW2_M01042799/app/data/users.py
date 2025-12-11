from app.data.db import connect_database
import os


# Insert a single user
def insert_user(username, password_hash, role="user"):
    conn = connect_database()
    cur = conn.cursor()
    #Add new user to DB
    cur.execute("""
        INSERT INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
    """, (username, password_hash, role))
    conn.commit()
    conn.close()


# Get a user by username
def get_user_by_username(username):
    conn = connect_database()
    cur = conn.cursor()
    #Fetch single user
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()
    return user

# Import all users from users.txt
def import_users_txt(txt_path="DATA/users.txt"):
    #Check if txt file exists
    if not os.path.exists(txt_path):
        print(f"⚠ File not found: {txt_path}")
        return False

    conn = connect_database()
    cur = conn.cursor()

    #Read each line from txt
    with open(txt_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                #Split: username,password_hash
                username, password_hash = line.split(",", 1)
                cur.execute("""
                    INSERT OR IGNORE INTO users (username, password_hash)
                    VALUES (?, ?)
                """, (username, password_hash))
            except Exception as e:
                print(f"Error inserting user '{line}': {e}")

    conn.commit()
    conn.close()
    print("✔ Users imported successfully from users.txt")
    return True
