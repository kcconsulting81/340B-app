"""Vendor Contract Analyzer

Analyzes contract pharmacy and vendor agreements for ROI, utilization, and value.
Identifies underperforming locations and models financial impact of changes.
"""

import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="📄 Vendor Contract Analyzer", layout="wide")
st.title("📄 Vendor Contract Analyzer")

st.markdown("Upload vendor agreements, pharmacy performance reports, and fee schedules. "
            "This tool calculates ROI and highlights underperforming or low-utilization contracts.")

# File uploads
contract_file = st.file_uploader("📜 Upload Contract/Vendor Agreement Data", type=["xlsx", "csv"])
performance_file = st.file_uploader("📊 Upload Contract Pharmacy Performance Report", type=["xlsx", "csv"])

def load_data(file):
    if not file:
        return pd.DataFrame()
    return pd.read_excel(file) if file.name.endswith("xlsx") else pd.read_csv(file)

contracts = load_data(contract_file)
performance = load_data(performance_file)

if not contracts.empty and not performance.empty:
    st.subheader("🔗 Merged Vendor & Performance Data")

    # Merge on Vendor or Pharmacy Store ID
    if "Store ID" in contracts.columns and "Store ID" in performance.columns:
        merged = pd.merge(performance, contracts, on="Store ID", how="left")
    elif "Vendor" in contracts.columns and "Vendor" in performance.columns:
        merged = pd.merge(performance, contracts, on="Vendor", how="left")
    else:
        st.warning("⚠️ Could not match 'Store ID' or 'Vendor' columns between files.")
        merged = pd.DataFrame()

    if not merged.empty:
        if {"Gross Revenue", "Fee Paid ($)"}.issubset(merged.columns):
            merged["ROI (%)"] = (
                (merged["Gross Revenue"] - merged["Fee Paid ($)"]) / merged["Fee Paid ($)"]
            ) * 100
            merged["Profitability"] = merged["ROI (%)"].apply(
                lambda x: "Unprofitable" if x < 0 else "Marginal" if x < 50 else "Profitable"
            )

        st.dataframe(merged)

        st.download_button(
            label="⬇️ Download ROI Evaluation Report",
            data=merged.to_csv(index=False),
            file_name="vendor_contract_roi_analysis.csv",
            mime="text/csv"
        )

        st.subheader("🚨 Underperforming Contracts")
        flagged = merged[merged["Profitability"] == "Unprofitable"]
        st.dataframe(flagged)

        st.download_button(
            label="⬇️ Download Unprofitable Contracts",
            data=flagged.to_csv(index=False),
            file_name="underperforming_contracts.csv",
            mime="text/csv"
        )
else:
    st.info("Please upload both a contract/vendor file and a performance report to continue.")
