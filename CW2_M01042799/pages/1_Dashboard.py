import streamlit as st# web app framework for dashboards
import plotly.express as px# interactive charts

# Services
from app.services.incident_service import (
    fetch_incidents,#Get Cybersecurity incidents
    count_by_severity,#count incident by severity
    count_by_status,#count incident by status
    trend_over_time as trend_incidents,# get incident trend
)
from app.services.ticket_service import (
    fetch_tickets,#get all IT tickets
    count_by_priority,#count tickets by priority
    count_by_status as ticket_status_count,#count tickets by status
    trend_over_time as trend_tickets,#get ticket trend
    ticket_summary,#generate ticket summary
)


# PAGE CONFIG
st.set_page_config(
    page_title="Cyber + IT Dashboard",
    page_icon="🛡️🛠️",
    layout="wide"
)

st.title("🛡️ Cybersecurity & IT Service Dashboard")

# Load data from services
df_incidents = fetch_incidents()
df_tickets = fetch_tickets()

# Combined Key Metrics
col1, col2, col3, col4 = st.columns(4)#4 metrics side by side
col1.metric("Total Incidents", len(df_incidents))# total incidents
col2.metric("Open Incidents", len(df_incidents[df_incidents['status'].str.lower() == "open"]))#open incidents
col3.metric("Total Tickets", len(df_tickets))#total IT tickets
col4.metric("Open Tickets", len(df_tickets[df_tickets['status'].str.lower().isin(["open", "in progress"])]))#open/in progress tickets

st.divider()

# Cyber Incident Analytics
st.subheader("️ Cybersecurity Incidents")

# Incident Trends
trend_inc_df = trend_incidents(df_incidents)
if not trend_inc_df.empty:#only show if data exists
    fig = px.line(trend_inc_df, x="date", y="count", title="Incident Trend Over Time", markers=True)
    st.plotly_chart(fig, use_container_width=True)

# Severity & Status pie Charts
col1, col2 = st.columns(2)
with col1:
    severity_df = count_by_severity(df_incidents)
    if not severity_df.empty:
        fig = px.pie(severity_df, names='severity', values='count', title="Severity Distribution")
        st.plotly_chart(fig, use_container_width=True)
with col2:
    status_df = count_by_status(df_incidents)
    if not status_df.empty:
        fig = px.pie(status_df, names='status', values='count', title="Status Distribution")
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# IT Ticket Analytics
st.subheader(" IT Tickets")

# Ticket Trend Chart
trend_ticket_df = trend_tickets(df_tickets)
if not trend_ticket_df.empty:
    fig = px.line(trend_ticket_df, x="date", y="count", title="Ticket Trend Over Time", markers=True)
    st.plotly_chart(fig, use_container_width=True)

# Priority & Status Pie Charts
col1, col2 = st.columns(2)
with col1:
    priority_df = count_by_priority(df_tickets)
    if not priority_df.empty:
        fig = px.pie(priority_df, names='priority', values='count', title="Priority Distribution")
        st.plotly_chart(fig, use_container_width=True)
with col2:
    status_df = ticket_status_count(df_tickets)
    if not status_df.empty:
        fig = px.pie(status_df, names='status', values='count', title="Status Distribution")
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.divider()
st.caption("Cybersecurity & IT Service Dashboard • CST1510")
