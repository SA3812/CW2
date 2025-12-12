# import Streamlit for UI and dashboard
import streamlit as st
import plotly.express as px

# Services for incidents
from app.services.incident_service import (
    fetch_incidents,
    count_by_severity,
    count_by_status,
    trend_over_time,
    incident_summary,
    delete_incident,
)

# Data function for CSV $ insert
from app.data.incidents import import_csv_incidents, insert_incident

# PAGE CONFIG
st.set_page_config(page_title="Cyber Incidents", page_icon="📁", layout="wide")
st.title("📁 Cybersecurity Incident Management")

# SIDEBAR
with st.sidebar:
    st.header(" Options")

    # Import CSV button
    if st.button(" Import CSV Data"):
        success = import_csv_incidents()
        if success:
            st.success("CSV imported successfully!")
            st.rerun()
        else:
            st.error("CSV file not found or import failed.")

    st.divider()

    #Create new incident form
    st.header("➕ Create New Incident")
    with st.form("create_incident_form"):
        date = st.date_input("Date")
        incident_type = st.text_input("Incident Type")
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        status = st.selectbox("Status", ["Open", "Investigating", "Mitigated", "Closed"])
        description = st.text_area("Description")
        reported_by = st.text_input("Reported By", "manual")

        submitted = st.form_submit_button("Create Incident")

        if submitted:
            ok = insert_incident(
                str(date),
                incident_type,
                severity,
                status,
                description,
                reported_by,
            )
            if ok:
                st.success("Incident created successfully!")
                st.rerun()
            else:
                st.error("Failed to create incident.")



# Load incidents
df = fetch_incidents()
if df.empty:
    st.warning(" No incidents found in the database.")
    st.info("Try importing a CSV or create a new incident in the sidebar.")
    st.stop()

st.success(f"Loaded **{len(df)} incidents** from the database.")



# Display table
st.subheader(" Incident Records")
st.dataframe(df, use_container_width=True)

# DELETE INCIDENT
st.subheader("🗑️ Delete an Incident")

incident_ids = df["id"].tolist()
incident_to_delete = st.selectbox("Select Incident ID to delete:", incident_ids)

if st.button("Delete Incident"):
    if delete_incident(incident_to_delete):
        st.success(f"Incident {incident_to_delete} deleted successfully!")
        st.rerun()
    else:
        st.error("Failed to delete incident.")

#Summary text
st.subheader("📊 Summary")
summary = incident_summary(df)
st.text(summary)

#Analytics
st.subheader(" Incident Analytics")
col1, col2 = st.columns(2)

# Severity chart
with col1:
    st.markdown("### Severity Breakdown")
    severity_df = count_by_severity(df)
    if not severity_df.empty:
        st.bar_chart(severity_df.set_index("severity"))
    else:
        st.info("No severity data available.")

# Status chart
with col2:
    st.markdown("### Status Breakdown")
    status_df = count_by_status(df)
    if not status_df.empty:
        st.bar_chart(status_df.set_index("status"))
    else:
        st.info("No status data available.")


# Trend over time
st.markdown("###  Incident Trend Over Time ")
trend_df = trend_over_time(df)

if not trend_df.empty:
    fig = px.line(
        trend_df,
        x="date",
        y="count",
        markers=True,   # <-- THIS adds scatter dots
        title="Incident Trend Over Time",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No valid date data found.")

# Footer
st.divider()
st.caption("Cyber Incidents Dashboard • CST1510")
