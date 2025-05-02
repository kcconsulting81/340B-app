"""340B Contract Tracker

This module helps manage drug contracts by identifying expired, missing, or uncovered
NDCs based on uploaded contract and invoice files.
"""
from datetime import datetime, timedelta

import streamlit as st
import pandas as pd

st.set_page_config(page_title="340B Contract Tracker", layout="wide")
st.title("📑 340B Contract & Coverage Manager")

contract_file = st.file_uploader(
    "📄 Upload Contract File (NDCs, Dates, Account Types)",
    type=["xlsx", "csv"]
)
invoice_file = st.file_uploader(
    "💊 (Optional) Upload Invoice to Check Coverage",
    type=["xlsx", "csv"]
)

if contract_file:
    contracts = (
        pd.read_excel(contract_file)
        if contract_file.name.endswith("xlsx")
        else pd.read_csv(contract_file)
    )
    contracts["Start Date"] = pd.to_datetime(contracts["Start Date"])
    contracts["End Date"] = pd.to_datetime(contracts["End Date"])
    today = pd.to_datetime(datetime.today().date())

    st.subheader("📋 Contracts Preview")
    st.dataframe(contracts.head())

    contracts["Status"] = contracts["End Date"].apply(
        lambda x: (
            "❌ Expired"
            if x < today
            else ("⚠️ Expires Soon" if x < today + timedelta(days=30) else "✅ Active")
        )
    )

    st.subheader("📅 Contract Status by Account Type")
    st.dataframe(
        contracts[["NDC", "Account Type", "Wholesaler", "End Date", "Status"]]
    )

    if invoice_file:
        invoice = (
            pd.read_excel(invoice_file)
            if invoice_file.name.endswith("xlsx")
            else pd.read_csv(invoice_file)
        )

        merged = pd.merge(invoice, contracts, on="NDC", how="left")

    def coverage_flag(row):
        """Return contract coverage status for each invoice row based on contract matching."""
        if pd.isna(row["Wholesaler"]):
            return "❌ Not Under Any Contract"
        if row["End Date"] < today:
            return "❌ Contract Expired"
        return "✅ Covered"

    if invoice_file:
        merged["Contract Coverage Status"] = merged.apply(coverage_flag, axis=1)

        st.subheader("🔍 Invoice Coverage Validation")
        st.dataframe(
            merged[["NDC", "Drug Name", "Account Type_inv", "Contract Coverage Status"]]
        )

        st.download_button(
            label="⬇️ Download Coverage Report",
            data=merged.to_csv(index=False),
            file_name="contract_coverage_report.csv",
            mime="text/csv"
        )
