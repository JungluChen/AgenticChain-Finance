import streamlit as st
import time
from openai import OpenAI

def get_agent_reasoning(po_data, inventory_data, iot_data):
    """Call the NVIDIA NIM API for reasoning logic""" 
    try: 
        nvidia_api_key = st.secrets["secrets"]["NVIDIA_API_KEY"] if "secrets" in st.secrets else st.secrets["NVIDIA_API_KEY"]
    except KeyError: 
        st.error("NVIDIA_API_KEY is not set in .streamlit/secrets.toml!") 
        st.stop() 

    client = OpenAI( 
        base_url="https://integrate.api.nvidia.com/v1", 
        api_key=nvidia_api_key 
    ) 

    prompt = f"""
    Analyze the following manufacturing and supply chain data to determine if the current production state is safe or at risk.
    
    Data:
    - Purchase Order: {po_data['units']} units required.
    - Inventory: {inventory_data['raw_material']} units available.
    - IoT Uptime: {iot_data['uptime']}%
    
    Provide a brief risk assessment, highlight any anomalies or shortfalls, and give a recommendation.
    """ 
    
    try: 
        response = client.chat.completions.create( 
            model="meta/llama3-8b-instruct", 
            messages=[ 
                {"role": "system", "content": "You are a senior financial analyst and AI credit agent."}, 
                {"role": "user", "content": prompt} 
            ], 
            temperature=0.2, 
            max_tokens=500 
        ) 
        return response.choices[0].message.content 
    except Exception as e: 
        # Graceful fallback for demo purposes if API key or model fails 
        return f"**NVIDIA NIM Analysis (Demo Fallback - {e}):**\n\n- **Detected Gap:** The order exceeds available balance by exactly the shortfall amount.\n- **Risk Assessment:** Critical supply chain bottleneck. Failure to fund this PO immediately will delay production and incur late penalties.\n- **Recommendation:** Proceed to query lenders for short-term JIT financing to bridge this gap." 

def calculate_credit_score(po_data, inventory_data, iot_data, base_score=750):
    """
    Calculate dynamic credit score based on production metrics.
    Equation: Score = Base Score + (Inventory Coverage Ratio * 100) + (IoT Uptime % * 1.5) - Penalties
    Max score: 1000, Min score: 0
    """
    score = base_score
    
    # Inventory Coverage (max 100 points)
    if po_data['units'] > 0:
        coverage = min(1.0, inventory_data['raw_material'] / po_data['units'])
        score += int(coverage * 100)
    else:
        score += 100 # Default if no PO
        
    # IoT Uptime (max 150 points)
    score += int(iot_data['uptime'] * 1.5)
    
    # Penalties
    if inventory_data['raw_material'] < po_data['units']:
        score -= 100 # Shortfall penalty
        
    if iot_data['uptime'] < 90:
        score -= 150 # Downtime risk penalty
        
    # Cap between 0 and 1000
    return max(0, min(1000, score))

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
