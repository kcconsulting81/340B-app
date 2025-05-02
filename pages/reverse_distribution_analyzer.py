"""Reverse Distribution Analyzer

Analyzes INMAR reverse distributor reports to identify lost drugs, unrecoverable NDCs,
and patterns of high-expiration or return risks.
"""

import pandas as pd
import streamlit as st

st.set_page_config(page_title="♻️ Reverse Distribution Analyzer", layout="wide")
st.title("♻️ Reverse Distribution Analyzer")

st.markdown("Upload INMAR or reverse distributor reports to analyze NDCs lost to return, "
            "identify unrecoverable value, and suggest flags for alternatives or formulary review.")

reverse_file = st.file_uploader("📦 Upload Reverse Distribution Report", type=["xlsx", "csv"])
price_file = st.file_uploader("💰 Upload NDC Price File (optional)", type=["xlsx", "csv"])

if reverse_file:
    rev = (
        pd.read_excel(reverse_file)
        if reverse_file.name.endswith("xlsx")
        else pd.read_csv(reverse_file)
    )

    if price_file:
        price = (
            pd.read_excel(price_file)
            if price_file.name.endswith("xlsx")
            else pd.read_csv(price_file)
        )
        rev["NDC"] = rev["NDC"].astype(str)
        price["NDC"] = price["NDC"].astype(str)
        rev = pd.merge(rev, price[["NDC", "Unit Price ($)"]], on="NDC", how="left")
        rev["Lost Value ($)"] = rev["Quantity Returned"] * rev["Unit Price ($)"]

    rev["Recouped"] = rev["Return Status"].str.lower().str.contains("recoup")
    rev["Flag"] = ~rev["Recouped"]

    st.subheader("🔍 Returned Drug Analysis")
    st.dataframe(rev)

    st.download_button(
        "⬇️ Download Reverse Return Report",
        data=rev.to_csv(index=False),
        file_name="reverse_return_analysis.csv",
        mime="text/csv"
    )
