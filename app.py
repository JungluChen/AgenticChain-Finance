import streamlit as st
import pandas as pd
from utils.state import init_state

st.set_page_config(
    page_title="AgenticChain Finance MVP",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
# Custom CSS for Industrial Fintech theme
st.markdown("""
<style>
    .stApp {
        background-color: #0d1117;
    }
    .css-1d391kg {
        background-color: #161b22;
    }
    h1, h2, h3 {
        color: #58a6ff;
    }
    .trust-green {
        color: #2ea043;
        font-weight: bold;
    }
    .risk-red {
        color: #f85149;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

init_state()
st.title("🔗 AgenticChain Finance")
st.markdown("""
### Transforming Supply Chain Finance with Agentic AI & Blockchain
Welcome to the Proof of Concept for AgenticChain. This real-time simulation bridges the trust gap between SMEs (Manufacturers) and Banks by using an AI Agent to verify production physicals and secure them on a blockchain ledger.

---
**How to use this prototype:**
1. Navigate the sidebar to different modules (SME Operations, AI Auditor, Blockchain Ledger, Banker's Portal).
2. Start as the **Manufacturer** to load contracts and run operations.
3. Switch to the **AI Auditor** to watch the real-time reasoning engine.
4. Check the **Blockchain Ledger** to see immutable milestone anchors.
5. act as the **Banker** to view live credit scores and release funds.
""")

st.sidebar.success("Initialized AgenticChain Core modules.")
