import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
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
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.state import init_state, persist_state

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
                persist_state()
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

with st.expander("📊 View Scoring Equation & Details"):
    st.markdown(r"""
    **Dynamic Credit Score Equation:**
    $$
    \text{Score} = \underbrace{750}_{\text{Base}} + (\text{Inventory Coverage Ratio} \times 100) + (\text{IoT Uptime \%} \times 1.5) - \text{Penalties}
    $$

    *Penalties applied for raw material shortfall ($-100$) or significant machine downtime ($-150$).*
    """)
    
    po_data = st.session_state.po_data
    inv_data = st.session_state.inventory_data
    iot_data = st.session_state.iot_data
    
    coverage_ratio = min(1.0, inv_data['raw_material'] / po_data['units']) if po_data['units'] > 0 else 1.0
    st.write(f"- **Base Score:** 750")
    st.write(f"- **Inventory Component:** +{int(coverage_ratio * 100)} (Coverage: {coverage_ratio:.2f})")
    st.write(f"- **IoT Uptime Component:** +{int(iot_data['uptime'] * 1.5)} (Uptime: {iot_data['uptime']}%)")
    
    penalty = 0
    if inv_data['raw_material'] < po_data['units']:
        penalty -= 100
    if iot_data['uptime'] < 90:
        penalty -= 150
        
    if penalty < 0:
        st.write(f"- **Penalties Applied:** {penalty}")
    else:
        st.write(f"- **Penalties Applied:** None")

st.divider()

st.subheader("🔍 Critical Risk Indicators")

# 取得必要資料
inventory = st.session_state.inventory_data
po = st.session_state.po_data
iot = st.session_state.iot_data
ledger = st.session_state.ledger

# 計算關鍵指標
raw_material_shortfall = max(0, po['units'] - inventory['raw_material']) if po['units'] > 0 else 0
production_delay_risk = max(0, po['units'] - iot['produced']) if po['units'] > 0 else 0
ledger_gaps = max(0, po['units'] - len(ledger)) if po['units'] > 0 else 0

# 顯示關鍵指標卡片
col_ind1, col_ind2, col_ind3 = st.columns(3)

with col_ind1:
    if raw_material_shortfall > 0:
        st.error(f"⚠️ **Raw Material Shortfall:** {raw_material_shortfall} units")
    else:
        st.success("✅ Raw Material: Sufficient")

with col_ind2:
    if production_delay_risk > 0:
        st.warning(f"⏰ **Production Delay Risk:** {production_delay_risk} units behind")
    else:
        st.success("✅ Production: On Track")

with col_ind3:
    if ledger_gaps > 0:
        st.warning(f"📋 **Ledger Verification Gaps:** {ledger_gaps} units unverified")
    else:
        st.success("✅ Ledger: Fully Verified")

# 風險評分說明
with st.expander("📊 Risk Scoring Details"):
    st.markdown("""
    **Critical Risk Factors:**
    
    1. **Raw Material Coverage:** Current inventory vs PO requirements
       - Risk Level: High if shortfall > 10% of PO units
       - Impact: Production halt, financing risk
    
    2. **Production Progress:** Actual vs planned production
       - Risk Level: High if behind schedule > 20%
       - Impact: Delivery delays, penalty clauses
    
    3. **Ledger Verification:** Blockchain milestone coverage
       - Risk Level: High if unverified units > 15%
       - Impact: Smart contract failure, funding freeze
    
    **Current Status:**
    """)
    
    # 詳細風險分析
    if po['units'] > 0:
        material_risk_pct = (raw_material_shortfall / po['units']) * 100
        production_risk_pct = (production_delay_risk / po['units']) * 100
        ledger_risk_pct = (ledger_gaps / po['units']) * 100
        
        st.write(f"- **Material Risk:** {material_risk_pct:.1f}% ({'HIGH' if material_risk_pct > 10 else 'LOW'})")
        st.write(f"- **Production Risk:** {production_risk_pct:.1f}% ({'HIGH' if production_risk_pct > 20 else 'LOW'})")
        st.write(f"- **Verification Risk:** {ledger_risk_pct:.1f}% ({'HIGH' if ledger_risk_pct > 15 else 'LOW'})")
    else:
        st.info("No active PO to analyze")
