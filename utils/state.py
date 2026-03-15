import streamlit as st

def init_state():
    # Initialize basic info
    if "credit_score" not in st.session_state:
        st.session_state.credit_score = 750
    if "po_data" not in st.session_state:
        st.session_state.po_data = {"units": 0, "status": "No PO"}
    if "inventory_data" not in st.session_state:
        st.session_state.inventory_data = {"raw_material": 0}
    if "iot_data" not in st.session_state:
        st.session_state.iot_data = {"uptime": 100, "produced": 0, "status": "Idle"}
    if "ledger" not in st.session_state:
        st.session_state.ledger = []
    if "agent_logs" not in st.session_state:
        st.session_state.agent_logs = []
    if "anomaly_detected" not in st.session_state:
        st.session_state.anomaly_detected = False
    if "scenario" not in st.session_state:
        st.session_state.scenario = "A (Success)"
    if "funds_released" not in st.session_state:
        st.session_state.funds_released = False
