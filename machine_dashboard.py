from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AQUA-CLEAN Machine",
    page_icon="🌊",
    layout="wide"
)
st_autorefresh(
    interval=5000,
    key="machine_dashboard_refresh"
)

st.title("🌊 AQUA-CLEAN AI")
st.subheader("Autonomous Lake Cleaning Machine")

import os

DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "hotspots.csv"
)

hotspots = pd.read_csv(DATA_FILE)

hotspots.columns = hotspots.columns.str.strip().str.lower()

hotspots = hotspots.rename(columns={
    "hotspot_id": "Hotspot ID",
    "latitude": "Latitude",
    "longitude": "Longitude",
    "waste": "Waste",
    "priority": "Priority",
    "status": "Status"
})

st.caption("Machine Control Dashboard | Prototype")


# Read hotspot data shared by the drone
import os

DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "hotspots.csv"
)

if os.path.exists(DATA_FILE):
    hotspots = pd.read_csv(DATA_FILE)
else:
    st.error("hotspots.csv not found in the project folder.")
    st.stop()

if hotspots.empty:
    st.warning("No hotspots have been reported by the drone yet.")
    st.stop()

    
# Store task status
if "status" not in st.session_state:
    st.session_state.status = "Waiting for task"

st.divider()

# Machine overview
st.markdown("### Machine Overview")

a, b, c = st.columns(3)
a.metric("Battery", "85% (Demo)")
b.metric("Waste Bin", "20% (Demo)")
c.metric("Connection", "Simulation")

st.divider()

# Hotspot list
st.markdown("### 📍 Available Cleaning Hotspots")
st.dataframe(hotspots, use_container_width=True)


#
# Task assignment
st.markdown("### 🎯 Assign a Cleaning Task")

hotspot = st.selectbox(
    "Choose hotspot",
    hotspots["hotspot_id"].astype(str).tolist()
)

selected = hotspots[
    hotspots["hotspot_id"].astype(str) == hotspot
].iloc[0]

st.write("Waste type:", selected["waste"])
st.write("Priority:", selected["priority"])
st.write(
    "Coordinates:",
    selected["latitude"],
    selected["longitude"]
)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Accept Task", use_container_width=True):
        st.session_state.status = "Task Accepted"
        st.rerun()

with col2:
    if st.button("Start Cleaning", use_container_width=True):
        if st.session_state.status == "Task Accepted":
            st.session_state.status = "Cleaning in Progress"
            st.rerun()
        else:
            st.warning("Accept the task first.")

with col3:
    if st.button("Mark Completed", use_container_width=True):
        if st.session_state.status == "Cleaning in Progress":
            st.session_state.status = "Completed"
            st.rerun()
        else:
            st.warning("Start cleaning first.")

st.divider()

st.caption("AQUA-CLEAN AI | Machine Dashboard")
st.caption("Hackathon prototype — sample data, not live machine telemetry.")
