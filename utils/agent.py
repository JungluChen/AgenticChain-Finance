import streamlit as st
import time

def run_agent_reasoning(scenario):
    st.session_state.agent_logs = []
    
    def add_log(msg):
        st.session_state.agent_logs.append(msg)
        time.sleep(1) # simulate thinking
        
    add_log("🤖 Agent initialized. Ingesting manufacturing data streams...")
    
    # 1. Check PO
    po = st.session_state.po_data
    if po["units"] == 0:
        add_log("⚠️ No active Purchase Order detected. Standing by.")
        return False
    add_log(f"✅ Ingested Purchase Order: {po['units']} units required.")
    
    # 2. Check Inventory
    inv = st.session_state.inventory_data
    add_log(f"🔍 Analyzing raw material inventory: {inv['raw_material']} available.")
    
    if inv["raw_material"] < po["units"]:
        add_log(f"🚨 ANOMALY DETECTED: Insufficient inventory to fulfill PO. Shortfall: {po['units'] - inv['raw_material']} units.")
        st.session_state.anomaly_detected = True
        return False
        
    add_log("✅ Sufficient inventory confirmed for production.")
    
    # 3. Check IoT Uptime
    iot = st.session_state.iot_data
    add_log(f"🏭 Connecting to IoT Machine Heartbeats... Uptime at {iot['uptime']}%.")
    
    if scenario == "B (Risk)" or iot["uptime"] < 90:
        add_log(f"🚨 ANOMALY DETECTED: Significant machine downtime detected (Uptime: {iot['uptime']}%). Production risk high.")
        st.session_state.anomaly_detected = True
        return False
        
    add_log("✅ Machine uptime is within nominal parameters (>90%).")
    add_log("🧠 Cross-Verification Complete. All systems nominal. Milestone ready for hashing.")
    return True
