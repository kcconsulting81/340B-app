"""Main App Launcher with Grouped Tabs for 340B Program Manager"""

import streamlit as st
import os
import pandas as pd

st.set_page_config(page_title="340B Program Manager", layout="wide")
st.title("🏥 340B Program Manager")

st.markdown(
    "Welcome to your centralized 340B program management platform. Select a tab to explore "
    "compliance tools, financial analytics, operational modules, or audit preparation."
)

# Optional dashboard summary
library_path = "library"
claim_file = os.path.join(library_path, "compliance_flags.csv")
contract_file = os.path.join(library_path, "contract_pharmacies.csv")

claims_df = pd.read_csv(claim_file) if os.path.exists(claim_file) else pd.DataFrame()
contracts_df = pd.read_csv(contract_file) if os.path.exists(contract_file) else pd.DataFrame()

st.subheader("📊 Program Summary Metrics")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Claims", f"{len(claims_df):,}")
with col2:
    flagged = claims_df["Flag"].value_counts().get("Yes", 0) if "Flag" in claims_df.columns else 0
    st.metric("Compliance Flags", f"{flagged:,}")
with col3:
    stores = contracts_df["Store ID"].nunique() if not contracts_df.empty else 0
    st.metric("Contract Pharmacies", f"{stores:,}")

# Grouped Module Launcher
st.subheader("🧭 Navigation")

tabs = st.tabs([
    "Compliance & Claims", "Financial Tools",
    "Program Operations", "Audit & Risk"
])

with tabs[0]:
    st.markdown("### 🔍 Compliance & Claims")
    st.button("Compliance Screener", on_click=lambda: os.system("streamlit run pages/6_🛡️_Compliance_Screener.py"))
    st.button("Claims Validator", on_click=lambda: os.system("streamlit run pages/4_🧾_Claims_Validator.py"))
    st.button("Lookback Impact Modeler", on_click=lambda: os.system("streamlit run pages/15_🕒_Lookback_Impact_Modeler.py"))

with tabs[1]:
    st.markdown("### 💰 Financial Tools")
    st.button("Invoice Checker", on_click=lambda: os.system("streamlit run pages/2_💰_Invoice_Checker.py"))
    st.button("Waste Recovery", on_click=lambda: os.system("streamlit run pages/12_🧮_Waste_Recovery_Calculator.py"))
    st.button("Vendor Contract Analyzer", on_click=lambda: os.system("streamlit run pages/17_📄_Vendor_Contract_Analyzer.py"))

with tabs[2]:
    st.markdown("### 🧠 Program Operations")
    st.button("NDC Migration Manager", on_click=lambda: os.system("streamlit run pages/3_🔄_NDC_Migration.py"))
    st.button("Rule Library", on_click=lambda: os.system("streamlit run pages/9_📚_Rule_Library_Builder.py"))
    st.button("Document Library", on_click=lambda: os.system("streamlit run pages/10_📂_Document_Library.py"))

with tabs[3]:
    st.markdown("### 🛡️ Audit & Risk")
    st.button("Audit Request Generator", on_click=lambda: os.system("streamlit run pages/19_📑_Audit_Request_Response_Generator.py"))
    st.button("Risk Analyzer & RCA", on_click=lambda: os.system("streamlit run pages/20_🛡️_Audit_Risk_Analyzer_and_RCA_Generator.py"))
    st.button("Change Evaluation Toolkit", on_click=lambda: os.system("streamlit run pages/18_📝_Change_Evaluation_Toolkit.py"))
