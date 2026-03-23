import streamlit as st
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
from utils.state import init_state

init_state()

st.title("🔗 Blockchain Trust Layer")
st.markdown("Immutable record of production milestones verified by the AI Auditor.")

if len(st.session_state.ledger) == 0:
    st.info("No milestones anchored yet. Run the AI Auditor to verify production and generate hashes.")
else:
    df = pd.DataFrame(st.session_state.ledger)
    st.dataframe(df, width='stretch')
    
    st.subheader("Verification Tool")
    selected_tx = st.selectbox("Select Transaction ID to verify", df["Transaction ID"].tolist())
    if st.button("Verify on Ledger"):
        with st.spinner("Connecting to simulated network..."):
            import time
            time.sleep(1.5)
            row = df[df["Transaction ID"] == selected_tx].iloc[0]
            st.success(f"✅ Hash `{row['Data Hash']}` matches network state. Milestone '{row['Milestone']}' is verified and immutable.")
