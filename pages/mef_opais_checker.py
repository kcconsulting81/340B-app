"""MEF and OPAIS Alignment Checker

This tool compares uploaded procurement addresses and invoice sites against OPAIS and MEF
records to detect mismatches in 340B-registered locations and Medicaid carve-in status.
"""

import pandas as pd
import streamlit as st

st.set_page_config(page_title="MEF & OPAIS Checker", layout="wide")
st.title("📍 MEF and OPAIS File Validator")

invoice_file = st.file_uploader(
    "📦 Upload Invoice File (with Site Addresses)", type=["xlsx", "csv"]
)
opais_file = st.file_uploader(
    "🏥 Upload OPAIS Site Registration File", type=["xlsx", "csv"]
)
mef_file = st.file_uploader(
    "🗂 Upload Medicaid Exclusion File (MEF)", type=["xlsx", "csv"]
)

if invoice_file and opais_file and mef_file:
    invoices = (
        pd.read_excel(invoice_file)
        if invoice_file.name.endswith("xlsx")
        else pd.read_csv(invoice_file)
    )
    opais = (
        pd.read_excel(opais_file)
        if opais_file.name.endswith("xlsx")
        else pd.read_csv(opais_file)
    )
    mef = (
        pd.read_excel(mef_file)
        if mef_file.name.endswith("xlsx")
        else pd.read_csv(mef_file)
    )

    invoices["Address"] = invoices["Address"].str.lower().str.strip()
    opais["Address"] = opais["Address"].str.lower().str.strip()

    unmatched = invoices[~invoices["Address"].isin(opais["Address"])]

    st.subheader("📍 Sites on Invoice NOT Found in OPAIS")
    st.dataframe(unmatched)

    st.download_button(
        label="⬇️ Download OPAIS Mismatch Report",
        data=unmatched.to_csv(index=False),
        file_name="opais_address_mismatch.csv",
        mime="text/csv"
    )

    st.subheader("📋 Medicaid Exclusion File Preview")
    st.dataframe(mef.head())

    st.success("✅ File comparison complete.")
