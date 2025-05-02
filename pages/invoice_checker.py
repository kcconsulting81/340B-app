"""340B Invoice Checker

This module compares wholesaler invoice prices against 340B ceiling prices
to identify potential overcharges and pricing discrepancies.
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Invoice Price Validator", layout="wide")
st.title("💰 340B Invoice Overcharge Checker")

invoice_file = st.file_uploader(
    "📄 Upload Invoice File",
    type=["xlsx", "csv"]
)
price_file = st.file_uploader(
    "💸 Upload 340B Ceiling Price File",
    type=["xlsx", "csv"]
)

if invoice_file and price_file:
    invoice_df = (
        pd.read_excel(invoice_file)
        if invoice_file.name.endswith("xlsx")
        else pd.read_csv(invoice_file)
    )
    price_df = (
        pd.read_excel(price_file)
        if price_file.name.endswith("xlsx")
        else pd.read_csv(price_file)
    )

    st.subheader("📦 Invoice Preview")
    st.dataframe(invoice_df.head())

    st.subheader("📈 Ceiling Price Preview")
    st.dataframe(price_df.head())

    merged = pd.merge(invoice_df, price_df, on="NDC", how="left")

    merged["Overcharged"] = merged["Unit Price"] > merged["Ceiling Price"]
    merged["Overcharge Amount"] = (
        merged["Unit Price"] - merged["Ceiling Price"]
    ).clip(lower=0)

    overcharged = merged[merged["Overcharged"]]

    st.subheader("⚠️ Overcharged Items")
    st.dataframe(overcharged)

    st.download_button(
        label="⬇️ Download Overcharge Report",
        data=overcharged.to_csv(index=False),
        file_name="overcharge_report.csv",
        mime="text/csv"
    )
