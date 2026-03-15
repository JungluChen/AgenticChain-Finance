import streamlit as st
import time
import sys
import os
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 針對右下角所有懸浮元件的強制隱藏
hide_streamlit_cloud_elements = """
    <style>
    /* 1. 隱藏右上角選單與工具欄 */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 2. 隱藏頁尾 "Made with Streamlit" */
    footer {visibility: hidden;}

    /* 3. 隱藏右下角 "Manage app" 黑色按鈕 */
    .stAppDeployButton {
        display: none !important;
    }

    /* 4. 隱藏右下角 "Hosted with Streamlit" 紅色標籤 (針對 Cloud 注入) */
    div[data-testid="stStatusWidget"] {
        visibility: hidden !important;
        display: none !important;
    }

    /* 5. 萬用：針對任何在底部右側出現的懸浮容器 */
    [data-testid="stConnectionStatus"],
    .st-emotion-cache-1wb5477, 
    .st-emotion-cache-6qob1r {
        display: none !important;
    }
    </style>
    """

st.markdown(hide_streamlit_cloud_elements, unsafe_allow_html=True)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.state import init_state
from utils.agent import run_agent_reasoning
from utils.blockchain import record_milestone

init_state()

st.title("🤖 Agentic Reasoning Engine")
st.markdown("The AI Auditor verifies physical operations against financial obligations in real-time.")

if st.button("Run AI Audit Cycle"):
    st.session_state.anomaly_detected = False
    with st.spinner("Agent is analyzing streams..."):
        # Placeholder for logs
        log_container = st.empty()
        
        # We simulate streaming output
        st.session_state.agent_logs = []
        def refresh_logs():
            log_text = "\n\n".join(st.session_state.agent_logs)
            log_container.info(log_text)
            
        # Manually run the agent logic step-by-step for UI effect
        st.session_state.agent_logs.append("🤖 Agent initialized. Ingesting manufacturing data streams...")
        refresh_logs()
        time.sleep(1)
        
        po = st.session_state.po_data
        st.session_state.agent_logs.append(f"✅ Ingested Purchase Order: {po['units']} units required.")
        refresh_logs()
        time.sleep(1)
        
        inv = st.session_state.inventory_data
        st.session_state.agent_logs.append(f"🔍 Analyzing raw material inventory: {inv['raw_material']} available.")
        refresh_logs()
        time.sleep(1)
        
        passed_inventory = True
        if inv["raw_material"] < po["units"]:
            st.session_state.agent_logs.append(f"🚨 ANOMALY DETECTED: Insufficient inventory to fulfill PO. Shortfall: {po['units'] - inv['raw_material']} units.")
            passed_inventory = False
            st.session_state.anomaly_detected = True
            
        refresh_logs()
        time.sleep(1)
        
        passed_iot = True
        iot = st.session_state.iot_data
        st.session_state.agent_logs.append(f"🏭 Connecting to IoT Machine Heartbeats... Uptime at {iot['uptime']}%.")
        refresh_logs()
        time.sleep(1)
        
        if "Risk" in st.session_state.scenario or iot["uptime"] < 90:
            st.session_state.agent_logs.append(f"🚨 ANOMALY DETECTED: Significant machine downtime. Production risk high.")
            passed_iot = False
            st.session_state.anomaly_detected = True
            
        refresh_logs()
        time.sleep(1)
        
        if passed_inventory and passed_iot:
            st.session_state.agent_logs.append("🧠 Cross-Verification Complete. Systems nominal. Anchoring milestone...")
            refresh_logs()
            time.sleep(1)
            
            # Record milestone
            hash_val = record_milestone(f"Verified Production: PO for {po['units']} units. Uptime {iot['uptime']}%.")
            st.session_state.agent_logs.append(f"🔗 Ledger Anchor Created. Hash: {hash_val}")
            
            # Increase credit score
            st.session_state.credit_score = min(1000, st.session_state.credit_score + 50)
            st.success("✅ Audit passed! Milestone recorded on ledger and credit score boosted.")
        else:
            # Drop credit score
            st.session_state.credit_score = max(0, st.session_state.credit_score - 100)
            st.error("❌ Audit failed due to anomalies. Score penalized. Banker alerts triggered.")
        
        refresh_logs()
