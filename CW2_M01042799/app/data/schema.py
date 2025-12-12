# app/data/schema.py
from app.data.db import connect_database

def create_users_table():
    conn = connect_database()
    cur = conn.cursor()
    #Create users table if missing
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def create_cyber_incidents_table():
    conn = connect_database()
    cur = conn.cursor()
    #Create incidents table if missing
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            incident_type TEXT,
            severity TEXT,
            status TEXT,
            description TEXT,
            reported_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def create_tickets_table():
    conn = connect_database()
    cur = conn.cursor()
    #Create tickets table if missing
    cur.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            status TEXT,
            assigned_to TEXT,
            priority TEXT,
            created_at TEXT,
            resolved_at TEXT,
            resolution_minutes INTEGER,
            created_by TEXT,
            updated_at TEXT
        )
    """)
    conn.commit()
    conn.close()

#Create all tables
def create_all_tables():
    create_users_table()
    create_cyber_incidents_table()
    create_tickets_table()

