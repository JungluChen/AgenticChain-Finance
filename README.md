# AgenticChain Finance

**AgenticChain Finance** is an Antigravity Finance MVP built using Streamlit. It is a multi-page application that simulates a secure, real-time trust loop between a Manufacturer (SME), an AI Auditor, and a Lender (Bank). 

## 🚨 The Pain Point in SME Financing
**The core problem:** Traditional JIT (Just-in-Time) or Supply Chain Financing suffers from a massive **trust and data gap**. 
- **For SMEs (Manufacturers):** They often struggle to get favorable credit terms because they cannot prove their real-time operational health or production milestones reliably to banks.
- **For Lenders (Banks):** They lack visibility into the ground-truth data of an SME's factory floor. Relying on manually reported, easily manipulated, or outdated financial statements increases lending risk, leading to higher interest rates or credit denial.

**The Solution:** By combining AI-driven auditing with a deterministic blockchain-based ledger, **AgenticChain Finance** bridges this trust gap. It ingests machine-level operations data, allows an AI to verify the production milestones, and securely anchors these findings on a tamper-proof ledger, enabling banks to issue dynamic, risk-adjusted loans in real time.

## ✨ Core Features
- **🏭 SME Operations Portal:** Simulates real-time manufacturing data, including Purchase Orders, Inventory, and IoT Machine Heartbeats.
- **🤖 AI Auditor Agent:** Powered by LangChain, this agent ingests and logically reasons about the simulated manufacturing data to verify milestones and detect anomalies.
- **🔗 Blockchain Ledger:** Simulates a tamper-proof trust layer by generating SHA-256 hashes of verified production milestones and appending them to a transparent ledger.
- **🏦 Banker Portal & Dynamic Credit Score:** A dynamic "Live Credit Score" gauge that reacts in real-time to the AI Agent's findings—dropping upon discovering anomalies and rising when milestones are successfully verified.
- **Sleek UI/UX:** Adheres to a clean, professional "Industrial Fintech" style using Streamlit, complete with a sidebar for persona switching and Plotly for intuitive data visualization.

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JungluChen/AgenticChain-Finance.git
   cd AgenticChain-Finance
   ```

2. **Install dependencies:**
   Ensure you are using Python 3.8+ and install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   Launch the interactive Streamlit dashboard:
   ```bash
   streamlit run app.py
   ```
