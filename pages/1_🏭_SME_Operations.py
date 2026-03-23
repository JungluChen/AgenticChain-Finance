import streamlit as st
import time
import random
import sys
import os
st.set_page_config(
    layout="wide",
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 針對右下角所有懸浮元件的強制隱藏
hide_streamlit_cloud_elements = """
    <style>
    /* 1. 隱藏右上角選單與工具欄 */
    #MainMenu {visibility: hidden;}
    
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
# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.state import init_state, persist_state

init_state()

st.title("🏭 SME Operations Dashboard")
st.markdown("**(Persona: SME Manager)** - Manage your production, ERP data, and IoT feeds.")

# Control Panel
st.sidebar.header("Simulation Settings")
scenario = st.sidebar.radio("Mock Scenario", ["A (Success)", "B (Risk)"])
st.session_state.scenario = scenario

col1, col2 = st.columns(2)

with col1:
    st.header("ERP Data Upload")
    po_input = st.number_input("Purchase Order Units Required", min_value=0, value=1000, step=100)
    inventory_input = st.number_input("Current Raw Material Inventory", min_value=0, value=1200 if "Success" in scenario else 800, step=100)
    
    if st.button("Sync ERP Data",width="stretch",type="primary"):
        st.session_state.po_data = {"units": po_input, "status": "Active"}
        st.session_state.inventory_data = {"raw_material": inventory_input}
        persist_state()
        st.success("✅ ERP Data Synchronized successfully.")
        # st.write(st.session_state.po_data)
        # st.write(st.session_state.inventory_data)

with col2:
    st.header("IoT Factory Feed")
    st.metric("Machine Uptime", f"{st.session_state.iot_data['uptime']}%", delta="Normal" if st.session_state.iot_data['uptime'] > 90 else "- Risk", delta_color="normal" if st.session_state.iot_data['uptime'] > 90 else "inverse")
    st.metric("Units Produced", st.session_state.iot_data['produced'])
    
    if st.button("Start Production Simulation", width="stretch", type="primary"):
        st.session_state.anomaly_detected = False # Reset
        with st.spinner("Simulating Factory Operations..."):
            for i in range(1, 6):
                time.sleep(0.5)
                # update state 
                uptime_val = random.randint(95, 100) if "Success" in scenario else random.randint(70, 85)
                produced_val = int((i/5.0) * st.session_state.po_data['units'] * (uptime_val/100.0))
                
                st.session_state.iot_data = {"uptime": uptime_val, "produced": produced_val, "status": "Running"}
        persist_state()
        st.success("🏁 Production cycle completed.")
        st.rerun()
