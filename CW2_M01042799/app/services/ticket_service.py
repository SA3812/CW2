# app/services/ticket_service.py
import pandas as pd
from app.data.tickets import get_all_tickets
from app.data.db import connect_database

# Fetch tickets
def fetch_tickets():
    # Get all tickets from the data layer
    return get_all_tickets()

# Count tickets by priority level
def count_by_priority(df: pd.DataFrame):
    #If no tickets, return empty structure for charts
    if df.empty:
        return pd.DataFrame({"priority": [], "count": []})

    #Count how many tickets exist per priority
    counts = df["priority"].value_counts().reset_index()
    #Rename columns to consistent names for Streamlit charts
    counts.columns = ["priority", "count"]
    return counts

# Status Count
def count_by_status(df: pd.DataFrame):
    #Handle empty datasets safely
    if df.empty:
        return pd.DataFrame({"status": [], "count": []})

    #Count each ticket status
    counts = df["status"].value_counts().reset_index()
    counts.columns = ["status", "count"]
    return counts

# Performance by Staff
def performance_by_staff(df: pd.DataFrame):
    #If no ticket data exists, return empty table
    if df.empty:
        return pd.DataFrame({"assigned_to": [], "avg_resolution_time": []})

    # Convert resolution time from minutes to hours
    if "resolution_minutes" in df.columns:
        df["resolution_time_hours"] = pd.to_numeric(df["resolution_minutes"], errors="coerce") / 60.0

    # Remove rows missing assigned staff or resolution time
    tmp = df.dropna(subset=["assigned_to", "resolution_time_hours"])
    # If no valid data remains, return empty structure
    if tmp.empty:
        return pd.DataFrame({"assigned_to": [], "avg_resolution_time": []})

    # Group by staff member and calculate average resolution time
    result = (
        tmp.groupby("assigned_to")["resolution_time_hours"]
        .mean()
        .reset_index()
        .rename(columns={"resolution_time_hours": "avg_resolution_time"})
        .sort_values("avg_resolution_time", ascending=False)
    )
    #Round values for clean display
    result["avg_resolution_time"] = result["avg_resolution_time"].round(2)
    return result

# Trend Over Time
def trend_over_time(df: pd.DataFrame):
    # Handle empty dataset safely
    if df.empty:
        return pd.DataFrame({"date": [], "count": []})

    #Convert raw timestamps to datetime objects
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    #Fill missing/invalid timestamps using current date
    df["created_at"] = df["created_at"].fillna(pd.Timestamp.today())
    #Extract date only (year-month-day)
    df["date"] = df["created_at"].dt.date
    #Count number of tickets per day
    trend = df.groupby("date").size().reset_index(name="count")
    #Convert date back to datetime for Streamlit charts
    trend["date"] = pd.to_datetime(trend["date"])
    return trend.sort_values("date")

# Summary
def ticket_summary(df: pd.DataFrame):
    #Handle no tickets case
    if df.empty:
        return "No tickets found in the system."

    #Total ticket count
    total = len(df)
    #Count by priority level
    high = (df["priority"] == "High").sum()
    critical = (df["priority"] == "Critical").sum()
    #Average resolution time
    avg_res = None
    if "resolution_minutes" in df.columns:
        avg_res = round(df["resolution_minutes"].mean() / 60.0, 2)

    # Return formatted summary string
    return (
        f"Total Tickets: {total}\n"
        f"High Priority: {high}\n"
        f"Critical Priority: {critical}\n"
        f"Average Resolution Time: {avg_res} hours\n"
    )


def delete_ticket(ticket_id: int):
    """Delete a ticket by its ID."""
    conn = connect_database()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM it_tickets WHERE id = ?", (ticket_id,))
        conn.commit()
        return True
    except Exception as e:
        print("Delete ticket error:", e)
        return False