import streamlit as st
import hashlib
import time
import uuid

def generate_milestone_hash(milestone_desc, po_units, uptime):
    # Combine data to create a unique hash
    raw_data = f"{milestone_desc}|{po_units}|{uptime}|{time.time()}"
    h = hashlib.sha256(raw_data.encode()).hexdigest()
    return h

def record_milestone(desc):
    po = st.session_state.po_data['units']
    uptime = st.session_state.iot_data['uptime']
    
    data_hash = generate_milestone_hash(desc, po, uptime)
    tx_id = "0x" + uuid.uuid4().hex
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    
    st.session_state.ledger.append({
        "Timestamp": timestamp,
        "Milestone": desc,
        "Data Hash": data_hash,
        "Transaction ID": tx_id
    })
    return data_hash
