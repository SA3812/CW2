# import Streamlit for UI and dashboard
import streamlit as st
import plotly.express as px

# Services for Ticket
from app.services.ticket_service import (
    fetch_tickets,
    count_by_priority,
    count_by_status,
    performance_by_staff,
    trend_over_time,
    ticket_summary,
    delete_ticket,
)

# Data functions for CSV & insert
from app.data.tickets import import_tickets_csv, insert_ticket

# Page config
st.set_page_config(page_title="IT Ticket Management", page_icon="🛠️", layout="wide")
st.title("🛠️ IT Service Desk - Ticket Management")

#Sidebar
with st.sidebar:
    st.header(" Options")
    #Import CSV button
    if st.button(" Import CSV Data"):
        success = import_tickets_csv("DATA/it_tickets.csv")
        if success:
            st.success("CSV imported successfully!")
            st.rerun()
        else:
            st.error("CSV file not found or import failed.")

    st.divider()
    #Create new ticket
    st.header("➕ Create New Ticket")

    with st.form("create_ticket_form"):
        title = st.text_input("Title")
        description = st.text_area("Description")
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
        assigned_to = st.text_input("Assigned To")

        submitted = st.form_submit_button("Create Ticket")

        if submitted:
            ok = insert_ticket(
                title=title,
                description=description,
                priority=priority,
                status=status,
                assigned_to=assigned_to
            )
            if ok:
                st.success("Ticket created successfully!")
                st.rerun()
            else:
                st.error("Failed to create ticket.")

#Load ticket data
df = fetch_tickets()

if df.empty:
    st.warning(" No tickets found in the database.")
    st.info("Try importing the CSV using the button in the sidebar, or create a ticket.")
    st.stop()

st.success(f"Loaded **{len(df)} tickets** from the database.")

#Display table
st.subheader(" Ticket Records")
st.dataframe(df, use_container_width=True)

# DELETE TICKET
st.subheader("🗑️ Delete a Ticket")

ticket_ids = df["id"].tolist()
ticket_to_delete = st.selectbox("Select a Ticket ID to Delete:", ticket_ids)

if st.button("Delete Ticket"):
    if delete_ticket(ticket_to_delete):
        st.success(f"Ticket {ticket_to_delete} deleted successfully!")
        st.rerun()
    else:
        st.error("Failed to delete ticket.")

#Summary text
st.subheader("📊 Summary")
summary = ticket_summary(df)
st.text(summary)

#Analytics charts
st.subheader(" Ticket Analytics")
col1, col2 = st.columns(2)

# Priority chart
with col1:
    st.markdown("### Priority Breakdown")
    priority_df = count_by_priority(df)

    if not priority_df.empty:
        st.bar_chart(priority_df.set_index("priority"))
    else:
        st.info("No priority data available.")

# Status chart
with col2:
    st.markdown("### Status Breakdown")
    status_df = count_by_status(df)

    if not status_df.empty:
        st.bar_chart(status_df.set_index("status"))
    else:
        st.info("No status data available.")


# Trend over time
st.markdown("###  Ticket Trend Over Time ")
trend_df = trend_over_time(df)

if not trend_df.empty:
    fig = px.line(
        trend_df,
        x="date",
        y="count",
        markers=True,  # <-- adds scatter dots
        title="Ticket Trend Over Time",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No valid date information available.")

#Footer
st.divider()
st.caption("IT Ticket Dashboard • CST1510")
