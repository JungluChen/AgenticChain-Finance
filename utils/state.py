import streamlit as st
from utils.db import init_db, load_state, load_ledger, save_state

def init_state():
    # Initialize database
    init_db()
    
    # Initialize basic info from DB
    if "credit_score" not in st.session_state:
        st.session_state.credit_score = load_state("credit_score", 750)
    if "po_data" not in st.session_state:
        st.session_state.po_data = load_state("po_data", {"units": 0, "status": "No PO"})
    if "inventory_data" not in st.session_state:
        st.session_state.inventory_data = load_state("inventory_data", {"raw_material": 0})
    if "iot_data" not in st.session_state:
        st.session_state.iot_data = load_state("iot_data", {"uptime": 100, "produced": 0, "status": "Idle"})
    if "ledger" not in st.session_state:
        st.session_state.ledger = load_ledger()
    if "agent_logs" not in st.session_state:
        st.session_state.agent_logs = []
    if "anomaly_detected" not in st.session_state:
        st.session_state.anomaly_detected = load_state("anomaly_detected", False)
    if "scenario" not in st.session_state:
        st.session_state.scenario = load_state("scenario", "A (Success)")
    if "funds_released" not in st.session_state:
        st.session_state.funds_released = load_state("funds_released", False)

def persist_state():
    save_state("credit_score", st.session_state.credit_score)
    save_state("po_data", st.session_state.po_data)
    save_state("inventory_data", st.session_state.inventory_data)
    save_state("iot_data", st.session_state.iot_data)
    save_state("anomaly_detected", st.session_state.anomaly_detected)
    save_state("scenario", st.session_state.scenario)
    save_state("funds_released", st.session_state.funds_released)
