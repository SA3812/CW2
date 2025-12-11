# app/services/incident_service.py

import pandas as pd
from app.data.incidents import get_all_incidents
from app.data.db import connect_database

# Fetch incident data through the service layer
def fetch_incidents():
    """Return all incidents using the data layer."""
    df = get_all_incidents()#Get incidents from database
    return df

# Basic Cybersecurity Analytics
def count_by_severity(df: pd.DataFrame):
    """Return a count of incidents by severity level."""
    if df.empty:
        return pd.DataFrame({"severity": [], "count": []})

    counts = df["severity"].value_counts().reset_index()
    counts.columns = ["severity", "count"]   # Fixed Column Names
    return counts

def count_by_status(df: pd.DataFrame):
    """Return a count of incidents by status."""
    if df.empty:
        return pd.DataFrame({"status": [], "count": []})

    counts = df["status"].value_counts().reset_index()
    counts.columns = ["status", "count"]    # Fixed Column Names
    return counts

def trend_over_time(df: pd.DataFrame):
    """Return incidents grouped by date for trend chart."""
    if df.empty:
        return pd.DataFrame({"date": [], "count": []})

    # Convert to datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Drop invalid dates
    df = df.dropna(subset=["date"])

    if df.empty:
        return pd.DataFrame({"date": [], "count": []})

    # Convert timestamp → date only (use .loc to avoid SettingWithCopyWarning)
    df.loc[:, "date"] = df["date"].dt.date

    # Group by date
    trend = df.groupby("date").size().reset_index(name="count")

    # Convert back to datetime for Streamlit chart
    trend["date"] = pd.to_datetime(trend["date"])

    return trend


def incident_summary(df: pd.DataFrame):
    """Simple automatic summary."""
    if df.empty:
        return "No incidents recorded."

    #Basic stats
    total = len(df)
    high = (df["severity"] == "High").sum()
    critical = (df["severity"] == "Critical").sum()

    #Text summary
    return (
        f"Total Incidents: {total}\n"
        f"High Severity: {high}\n"
        f"Critical Severity: {critical}\n\n"
        "This dashboard provides a basic cybersecurity overview.\n"
    )

def delete_incident(incident_id: int):
    """Delete an incident by its ID."""
    conn = connect_database()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
        conn.commit()
        return True
    except Exception as e:
        print("Delete error:", e)
        return False
