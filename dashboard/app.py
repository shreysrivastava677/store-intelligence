import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Store Intelligence Dashboard",
    layout="wide",
    page_icon="🏪"
)

# Refreshes the page every 5000 milliseconds (5 seconds)
st_autorefresh(
    interval=5000,
    key="refresh"
)

API_BASE = "http://127.0.0.1:8000"

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("🏪 Store Intelligence Dashboard")

# --------------------------------------------------
# API CALLS
# --------------------------------------------------
def get_data(endpoint):
    try:
        response = requests.get(
            f"{API_BASE}{endpoint}",
            timeout=5
        )
        return response.json()
    except Exception:
        # Returns an empty dictionary if the API is unreachable
        return {}

# Added a loading spinner for smoother UX during refresh cycles
with st.spinner("Fetching latest store intelligence..."):
    health = get_data("/health")
    summary = get_data("/analytics/zone-summary")
    zones = get_data("/analytics/zone-performance")
    anomalies = get_data("/stores/1/anomalies")

# --------------------------------------------------
# KPI ROW
# --------------------------------------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Total Events",
        health.get("total_events", 0) if health else 0
    )

with c2:
    st.metric(
        "Unique Visitors",
        summary.get("unique_visitors", 0) if summary else 0
    )

with c3:
    st.metric(
        "Zone Events",
        summary.get("total_zone_events", 0) if summary else 0
    )

# --------------------------------------------------
# HEALTH STATUS
# --------------------------------------------------
st.subheader("System Health")

# Fixed logic: Handles offline APIs correctly instead of defaulting to healthy
if not health:
    st.error("🔴 API OFFLINE / NO DATA")
elif health.get("stale_feed"):
    st.warning("🟡 STALE FEED DETECTED")
else:
    st.success("🟢 SYSTEM HEALTHY")

# --------------------------------------------------
# ZONE PERFORMANCE
# --------------------------------------------------
st.subheader("Zone Performance")

rows = []
if zones:
    for zone, values in zones.items():
        rows.append({
            "Zone": zone,
            "Visits": values.get("total_visits", 0),
            "Visitors": values.get("unique_visitors", 0)
        })

zone_df = pd.DataFrame(rows)

if not zone_df.empty:
    left, right = st.columns([1, 1])

    with left:
        st.dataframe(
            zone_df,
            use_container_width=True,
            hide_index=True 
        )

    with right:
        # Upgraded to Plotly for hover states, tooltips, and better styling
        fig = px.bar(
            zone_df, 
            x="Zone", 
            y="Visits", 
            color="Visits",
            color_continuous_scale="Blues",
            title="Visits by Zone"
        )
        fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No zone performance data available.")

# --------------------------------------------------
# ANOMALY DETECTION
# --------------------------------------------------
st.subheader("Anomaly Detection")

if anomalies:
    anomaly_list = anomalies.get("anomalies", [])

    if len(anomaly_list) == 0:
        st.success("✅ No active anomalies")
    else:
        # Wrapped in expanders to prevent UI clutter when multiple anomalies trigger
        for anomaly in anomaly_list:
            severity = anomaly.get("severity", "INFO")
            
            if severity == "CRITICAL":
                icon = "🚨"
            elif severity == "WARN":
                icon = "⚠"
            else:
                icon = "ℹ"

            with st.expander(f"{icon} {anomaly.get('type', 'Unknown')} - Zone: {anomaly.get('zone', 'Unknown')}"):
                st.write(f"**Description:** {anomaly.get('description', 'N/A')}")
                st.write(f"**Suggested Action:** {anomaly.get('suggested_action', 'N/A')}")
else:
    # If the endpoint fails, it falls back here safely
    st.success("✅ No active anomalies (or data unavailable)")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()

st.caption(
    f"Last Refresh: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)