
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ---------------------------------
# AQUA-CLEAN AI - Demo Dashboard
# ---------------------------------

st.set_page_config(
    page_title="AQUA-CLEAN AI",
    page_icon="🌊",
    layout="wide"
)

# Simple styling
st.markdown("""
<style>
.stApp {
    background-color: #f3faff;
}
h1, h2, h3 {
    color: #075985;
}
div[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #cce8f5;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# Demo data: illustrative lake zones, not live readings
zones = pd.DataFrame({
    "Zone": [
        "North Shore",
        "East Bank",
        "Central Lake",
        "South Shore",
        "West Inlet"
    ],
    "Latitude": [11.012, 11.008, 11.004, 10.999, 11.006],
    "Longitude": [76.955, 76.964, 76.958, 76.952, 76.947],
    "Pollution Index": [78, 42, 91, 56, 67],
    "Litter Items Detected": [34, 12, 48, 19, 27]
})

# Sidebar controls
st.sidebar.title("🌊 AQUA-CLEAN AI")
st.sidebar.caption("Smart Lake Monitoring Prototype")
st.sidebar.markdown("---")

threshold = st.sidebar.slider(
    "High-pollution threshold",
    min_value=30,
    max_value=100,
    value=70
)

selected_zone = st.sidebar.selectbox(
    "Select a lake zone",
    zones["Zone"].tolist()
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Prototype mode: this dashboard uses illustrative sample data. "
    "It is not connected to a real drone, camera, robot, or GPS."
)

# Header
st.title("🌊 AQUA-CLEAN AI")
st.subheader("AI-Powered Lake Pollution Monitoring & Cleaning")
st.caption(
    "Hackathon prototype | Smart Cities & Intelligent Mobility"
)

st.markdown("---")

# Calculate demo metrics
total_litter = int(zones["Litter Items Detected"].sum())
average_pollution = round(zones["Pollution Index"].mean())
high_priority = int((zones["Pollution Index"] >= threshold).sum())

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("🗑️ Demo litter detections", total_litter)
col2.metric("🌡️ Average pollution index", f"{average_pollution}/100")
col3.metric("📍 High-priority zones", high_priority)
col4.metric("🔋 Demo robot battery", "82%")

st.markdown("---")

# Main dashboard layout
left, right = st.columns([1.2, 1])

with left:
    st.subheader("📍 Lake Pollution Hotspot Map")
    st.write(
        "Each point represents an illustrative monitoring zone. "
        "The map uses sample coordinates."
    )

    map_data = zones.rename(columns={
        "Latitude": "lat",
        "Longitude": "lon"
    })

    st.map(map_data[["lat", "lon"]], zoom=12)

    st.caption(
        "Note: The coordinates are illustrative and may not represent "
        "your actual project lake."
    )

with right:
    st.subheader("📊 Pollution by Zone")

    chart = px.bar(
        zones,
        x="Zone",
        y="Pollution Index",
        color="Pollution Index",
        color_continuous_scale="YlOrRd",
        range_y=[0, 100],
        title="Illustrative pollution index (0–100)"
    )

    chart.update_layout(
        xaxis_title="Monitoring zone",
        yaxis_title="Pollution index",
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=50, b=10)
    )

    st.plotly_chart(chart, use_container_width=True)

# AI detection section
st.markdown("---")
st.header("🤖 AI Litter Detection — Demo")

selected_data = zones[zones["Zone"] == selected_zone].iloc[0]

d1, d2, d3 = st.columns(3)

d1.metric(
    "Selected zone",
    selected_zone
)

d2.metric(
    "Demo litter detections",
    int(selected_data["Litter Items Detected"])
)

d3.metric(
    "Pollution index",
    f'{int(selected_data["Pollution Index"])}/100'
)

if selected_data["Pollution Index"] >= threshold:
    st.warning(
        f"⚠️ {selected_zone} is marked as a high-priority zone "
        "in this demo."
    )
else:
    st.success(
        f"✅ {selected_zone} is below the selected demo threshold."
    )

st.info(
    "These results are simulated. A trained computer-vision model "
    "and real camera footage must be integrated for actual AI detection."
)

# Robot status
st.markdown("---")
st.header("🤖 Autonomous Cleaning Robot — Demo Status")

robot1, robot2 = st.columns(2)

with robot1:
    st.write("🔋 Battery level")
    st.progress(0.82)
    st.caption("82% — illustrative value")

with robot2:
    st.write("🧹 Cleaning mission progress")
    st.progress(0.46)
    st.caption("46% — illustrative value")

st.write("**Robot status:** Demo / simulated")
st.write("**Current mission:** Survey and identify priority zones")


# ---------------------------------
# AQUA-CLEAN AI Demo Alert Centre
# ---------------------------------

st.markdown("---")
st.header("🚨 Pollution Alert Centre")

# Keep demo alerts during Streamlit reruns
if "alerts" not in st.session_state:
    st.session_state.alerts = []

# Read the currently selected lake zone
selected_data = zones[zones["Zone"] == selected_zone].iloc[0]
selected_pollution = int(selected_data["Pollution Index"])

# Display the current zone status
if selected_pollution >= threshold:
    st.warning(
        f"⚠️ HIGH POLLUTION: {selected_zone} "
        f"({selected_pollution}/100)"
    )
else:
    st.success(
        f"✅ NORMAL STATUS: {selected_zone} "
        f"({selected_pollution}/100)"
    )


# ---------------------------------
# Automatic Pollution Alert System
# ---------------------------------

# Initialize alert history
if "alerts" not in st.session_state:
    st.session_state.alerts = []

# Track which zones have already triggered alerts
if "alerted_zones" not in st.session_state:
    st.session_state.alerted_zones = []

# Check all zones automatically whenever the dashboard reruns
for _, zone in zones.iterrows():
    zone_name = zone["Zone"]
    pollution = int(zone["Pollution Index"])

    if pollution >= threshold:
        if zone_name not in st.session_state.alerted_zones:
            message = (
                f"DEMO ALERT: {zone_name} pollution index is "
                f"{pollution}/100. Inspection is recommended."
            )

            st.session_state.alerts.insert(0, {
                "Time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "Zone": zone_name,
                "Pollution Index": pollution,
                "Status": "HIGH",
                "Message": message
            })

            st.session_state.alerted_zones.append(zone_name)

    else:
        # Allow a new alert if the zone later becomes high again
        if zone_name in st.session_state.alerted_zones:
            st.session_state.alerted_zones.remove(zone_name)

st.success("Automatic demo pollution monitoring is active.")

# Display current selected zone
st.subheader("🚨 Pollution Alert Centre")

selected_data = zones[zones["Zone"] == selected_zone].iloc[0]
selected_pollution = int(selected_data["Pollution Index"])

if selected_pollution >= threshold:
    st.warning(
        f"⚠️ {selected_zone}: HIGH pollution "
        f"({selected_pollution}/100)"
    )
else:
    st.success(
        f"✅ {selected_zone}: Pollution is below the threshold."
    )

# Alert history
st.subheader("📋 Demo Alert History")

if st.session_state.alerts:
    st.dataframe(
        pd.DataFrame(st.session_state.alerts),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No alerts generated yet.")

# Clear history and reset alert tracking
if st.button("🗑️ Clear Demo Alert History"):
    st.session_state.alerts = []
    st.session_state.alerted_zones = []
    st.rerun()

st.caption(
    "Demo simulation only. Automatic checks use sample data "
    "and do not send SMS or mobile notifications."
)


# Zone table
st.markdown("---")
st.header("📋 Monitoring Zone Details")

display_data = zones.copy()
display_data["Priority"] = display_data["Pollution Index"].apply(
    lambda value: "HIGH" if value >= threshold else "NORMAL"
)

st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True
)

# ---------------------------------
# Live-Style Monitoring Demo
# ---------------------------------

st.markdown("---")
st.header("📡 Live-Style Pollution Monitoring")

st.info(
    "Simulation mode: these readings are generated for demonstration. "
    "No real sensors are connected."
)

if "demo_pollution" not in st.session_state:
    st.session_state.demo_pollution = {
        "North Shore": 78,
        "East Bank": 42,
        "Central Lake": 91,
        "South Shore": 56,
        "West Inlet": 67
    }

if st.button("🔄 Simulate New Sensor Readings"):
    import random

    for zone_name in st.session_state.demo_pollution:
        change = random.randint(-8, 8)

        st.session_state.demo_pollution[zone_name] = max(
            0,
            min(
                100,
                st.session_state.demo_pollution[zone_name] + change
            )
        )

    st.success("Demo sensor readings updated!")

live_data = pd.DataFrame({
    "Zone": list(st.session_state.demo_pollution.keys()),
    "Pollution Index": list(st.session_state.demo_pollution.values())
})

st.dataframe(live_data, use_container_width=True, hide_index=True)

live_chart = px.bar(
    live_data,
    x="Zone",
    y="Pollution Index",
    color="Pollution Index",
    color_continuous_scale="YlOrRd",
    range_y=[0, 100],
    title="Simulated Sensor Readings"
)

st.plotly_chart(live_chart, use_container_width=True)


# Footer
st.markdown("---")
st.caption(
    "AQUA-CLEAN AI | NextGen Bender | KG College of Arts and Science"
)
st.caption(
    "Hackathon demonstration only — not for real-world environmental decisions."
)
st.markdown("---")

st.caption(
    "AQUA-CLEAN AI | NextGen Bender | KG College of Arts and Science"
)

st.caption(
    "Hackathon demonstration only – not for real-world environmental decisions."
)