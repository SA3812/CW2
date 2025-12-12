import pandas as pd
import os
from app.data.db import connect_database


def import_csv_incidents(csv_path="DATA/cyber_incidents.csv"):
    """Import incidents from CSV into DB """
    #Check if CSV exists
    if not os.path.exists(csv_path):
        print("CSV file not found:", csv_path)
        return False

    #Rename CSV into DataFrame
    df = pd.read_csv(csv_path)

    #Match CSV column name to database column names
    df.rename(columns={
        "timestamp": "date",
        "category": "incident_type"
    }, inplace=True)

    #connect to DB
    conn = connect_database()
    cur = conn.cursor()

    #Insert each row into DB
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO cyber_incidents 
            (date, incident_type, severity, status, description, reported_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row.get("date"),
            row.get("incident_type"),
            row.get("severity"),
            row.get("status"),
            row.get("description"),
            "system"
        ))

    #Save changes
    conn.commit()
    conn.close()
    return True

# Create new incident manually
def insert_incident(date, incident_type, severity, status, description, reported_by):
    try:
        conn = connect_database()
        cur = conn.cursor()

        #Insert a single incident
        cur.execute("""
            INSERT INTO cyber_incidents 
            (date, incident_type, severity, status, description, reported_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (date, incident_type, severity, status, description, reported_by))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print("Insert Incident Error:", e)
        return False

# Fetch all incidents
def get_all_incidents():
    conn = connect_database()
    #Return all rows as DataFrame
    df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
    conn.close()
    return df
