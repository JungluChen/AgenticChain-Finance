import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
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

init_state()

st.title("🏦 Banker's Portal")
st.markdown("**(Persona: Bank Officer)** - Monitor real-time dynamic risk and approve financing.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Live Credit Score")
    score = st.session_state.credit_score
    
    # Gauge Chart
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Dynamic Real-Time Score<br><span style='font-size:0.8em;color:gray'>Based on verified physicals</span>"},
        gauge = {
            'axis': {'range': [0, 1000]},
            'bar': {'color': "white"},
            'steps': [
                {'range': [0, 500], 'color': "#f85149"},
                {'range': [500, 800], 'color': "#d29922"},
                {'range': [800, 1000], 'color': "#2ea043"}],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': score}
        }
    ))
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    if st.session_state.anomaly_detected:
         st.error("🚨 ALERT: Anomaly detected by AI Auditor. Review immediately. Funding paused.")
    else:
        st.success("✅ Machine streams verified. Production operational.")
        
    st.subheader("Financing Approval Workflow")
    po = st.session_state.po_data
    
    if po["units"] > 0:
        st.write(f"**Active Request:** Financing for {po['units']} units.")
        
        milestones_verified = len(st.session_state.ledger) > 0
        
        if milestones_verified and not st.session_state.anomaly_detected and score >= 750:
            st.success("✅ Smart Contract conditions met. Production is backed by verified immutable ledger records.")
            if st.button("Release Funds / Execute Smart Contract"):
                st.session_state.funds_released = True
                st.balloons()
                st.success("💰 Funds Released to SME Wallet via Stablecoin!")
        elif st.session_state.anomaly_detected:
            st.warning("⚠️ Cannot release funds: production risk identified.")
            st.button("Release Funds / Execute Smart Contract", disabled=True)
        else:
            st.info("Awaiting production verification from AI Auditor. Minimum score 750, requiring at least 1 verified ledger anchor.")
            st.button("Release Funds / Execute Smart Contract", disabled=True)
    else:
        st.info("No active financing requests. SME needs to sync ERP data with an active Purchase Order.")


st.divider()
st.subheader("Risk Breakdown Charts")
r_col1, r_col2 = st.columns(2)

with r_col1:
    # Historical Fulfillment Reliability (dummy data)
    data_hist = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Current"],
        "Fulfillment %": [98, 95, 99, 100, 97, 100 if not st.session_state.anomaly_detected else 85]
    })
    fig_hist = px.bar(data_hist, x="Month", y="Fulfillment %", title="Historical Fulfillment Reliability", color="Fulfillment %", color_continuous_scale="greens")
    fig_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
    st.plotly_chart(fig_hist, use_container_width=True)

with r_col2:
    # Utilization vs Target
    po_units = st.session_state.po_data['units'] if st.session_state.po_data['units'] > 0 else 1000
    produced = st.session_state.iot_data['produced']
    
    data_util = pd.DataFrame({
        "Category": ["Produced", "Pending"],
        "Units": [produced, max(0, po_units - produced)]
    })
    fig_util = px.pie(data_util, names="Category", values="Units", title="Production Utilization vs Target", hole=0.4, color="Category", color_discrete_map={"Produced": "#58a6ff", "Pending": "#30363d"})
    fig_util.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
    st.plotly_chart(fig_util, use_container_width=True)
