import pandas as pd
import os
from app.data.db import connect_database


def import_tickets_csv(csv_path="DATA/it_tickets.csv"):
    """Import IT tickets from CSV into DB."""
    #Check if CSV exists
    if not os.path.exists(csv_path):
        print("CSV file not found:", csv_path)
        return False
    #Load CSV into DataFrame
    df = pd.read_csv(csv_path)

    #Connect to DB
    conn = connect_database()
    cur = conn.cursor()

    #Insert each row into DB
    for _, row in df.iterrows():
        cur.execute("""
            INSERT OR REPLACE INTO it_tickets 
            (id, title, description, status, assigned_to, priority, 
             created_at, resolved_at, resolution_minutes, created_by, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row.get("id"),
            row.get("title"),
            row.get("description"),
            row.get("status"),
            row.get("assigned_to"),
            row.get("priority"),
            row.get("created_at"),
            row.get("resolved_at"),
            row.get("resolution_minutes"),
            "system",
            row.get("updated_at"),
        ))

    conn.commit()
    conn.close()
    return True



# Create new ticket manually
def insert_ticket(title, description, status, assigned_to, priority, created_by="web"):
    try:
        conn = connect_database()
        cur = conn.cursor()

        #Insert new ticket
        cur.execute("""
            INSERT INTO it_tickets 
            (title, description, status, assigned_to, priority, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, description, status, assigned_to, priority, created_by))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Insert Ticket Error:", e)
        return False



# Fetch all tickets
def get_all_tickets():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    conn.close()
    return df
