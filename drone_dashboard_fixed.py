import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="AQUA-CLEAN AI", page_icon="🌊", layout="wide")

st.markdown("""
<style>
.stApp {background:linear-gradient(135deg,#00111f,#003047);color:#eaf7ff}
h1,h2,h3,p,label {color:#eaf7ff}
[data-testid="stMetric"] {background:#05283b;border:1px solid #087ca7;border-radius:12px;padding:12px}
[data-testid="stMetricValue"] {color:#43e6c1}
</style>
""", unsafe_allow_html=True)

header1, header2, header3 = st.columns([2, 2, 1.5])
with header1:
    st.title("🌊 AQUA-CLEAN AI")
    st.caption("Underwater Drone Monitoring System")
with header2:
    st.subheader("Drone Dashboard")
    st.caption("Cleaner Oceans • Healthier Tomorrow")
with header3:
    st.success("DEMO CONNECTED")
    st.caption(datetime.now().strftime("%d %b %Y · %H:%M"))

st.divider()

st.subheader("Demo controls")
col1, col2, col3, col4 = st.columns(4)
with col1:
    battery = st.slider("Battery remaining (%)", 0, 100, 68)
with col2:
    payload = st.slider("Collected waste (kg)", 0.0, 10.0, 3.4, 0.1)
with col3:
    depth = st.slider("Depth (m)", 0.0, 100.0, 12.6, 0.1)
with col4:
    temperature = st.slider("Water temperature (°C)", 0.0, 40.0, 24.8, 0.1)

runtime = int(135 * battery / 68) if battery else 0
runtime_text = f"{runtime // 60}h {runtime % 60}m"

left, middle, right = st.columns([2, 1, 1.15])

with left:
    st.subheader("🔴 Underwater Camera Feed")
    uploaded = st.file_uploader("Upload underwater image", type=["jpg", "jpeg", "png"])
    if uploaded:
        st.image(uploaded, use_container_width=True)
        st.info("Image preview only. An AI model is needed for actual plastic detection.")
    else:
        st.info("Upload an underwater photo to preview it here.")
    st.caption("Sample detections below are illustrative, not actual AI predictions.")
    st.subheader("🧪 Detected Objects (Sample)")
    a, b, c = st.columns(3)
    a.metric("Plastic bottle", "0.92", "Confidence")
    b.metric("Plastic bag", "0.87", "Confidence")
    c.metric("Metal can", "0.76", "Confidence")

with middle:
    st.subheader("🎯 Detection Summary")
    st.metric("♻️ Plastic detected", "12", "+3")
    st.metric("🧲 Metal detected", "4", "+1")
    st.metric("🐟 Invasive species", "2")
    st.metric("Pollution level", "HIGH")

with right:
    st.subheader("🚁 Drone Status")
    st.markdown("<div style='font-size:64px;text-align:center'>🚁</div>", unsafe_allow_html=True)
    st.write(f"🔋 Battery: **{battery}%**")
    st.progress(battery / 100)
    st.write(f"⏱️ Estimated runtime: **{runtime_text}**")
    st.write(f"⚖️ Payload: **{payload:.1f} / 10 kg**")
    st.progress(min(payload / 10, 1.0))
    st.write(f"🌊 Depth: **{depth:.1f} m**")
    st.write(f"🌡️ Water temperature: **{temperature:.1f} °C**")

g1, g2 = st.columns(2)
with g1:
    st.subheader("📈 Battery Trend (Sample)")
    chart = pd.DataFrame(
        {"Battery (%)": [100, 94, 86, 79, 73, battery]},
        index=["Start", "10 min", "20 min", "30 min", "40 min", "Now"]
    )
    st.line_chart(chart)
with g2:
    st.subheader("🕘 Recent Activity (Sample)")
    st.write("🟢 Plastic object detected — 2 min ago")
    st.write("🟠 Metal object detected — 4 min ago")
    st.write(f"🔵 Payload reading: {payload:.1f} kg — Now")
    st.write(f"🔋 Battery reading: {battery}% — Now")

st.divider()
st.caption("AQUA-CLEAN AI © 2026 | Demo prototype. All detections and telemetry are sample values, not live sensor readings.")
