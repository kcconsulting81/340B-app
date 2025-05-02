"""Waste Recovery Calculator
Calculates eligible waste from EPIC data and estimates recoverable 340B savings.
"""

import pandas as pd
import streamlit as st

st.set_page_config(page_title="🧮 Waste Recovery Calculator", layout="wide")
st.title("🧮 340B Waste Recovery Calculator")

st.markdown("Upload EPIC encounter and dispense reports to calculate recoverable drug waste "
            "and estimate 340B savings for wasted but billed doses.")

encounter_file = st.file_uploader("📥 Upload Encounter File", type=["xlsx", "csv"])
dispense_file = st.file_uploader("💉 Upload Dispense File", type=["xlsx", "csv"])
price_file = st.file_uploader("💰 Upload NDC Price File (optional)", type=["xlsx", "csv"])

if encounter_file and dispense_file:
    enc = (
        pd.read_excel(encounter_file)
        if encounter_file.name.endswith("xlsx")
        else pd.read_csv(encounter_file)
    )
    disp = (
        pd.read_excel(dispense_file)
        if dispense_file.name.endswith("xlsx")
        else pd.read_csv(dispense_file)
    )

    merged = pd.merge(enc, disp, on=["Encounter ID", "NDC"], how="inner")

    merged["Waste (mg)"] = (
        merged["Vial Size (mg)"] * merged["Vials Dispensed"]
    ) - merged["Dose Administered (mg)"]

    if price_file:
        price = (
            pd.read_excel(price_file)
            if price_file.name.endswith("xlsx")
            else pd.read_csv(price_file)
        )
        price["NDC"] = price["NDC"].astype(str)
        merged["NDC"] = merged["NDC"].astype(str)
        merged = pd.merge(merged, price[["NDC", "Unit Price ($)"]], on="NDC", how="left")
        merged["Savings ($)"] = merged["Waste (mg)"] * merged["Unit Price ($)"]

    st.subheader("📊 Waste Recovery Detail")
    st.dataframe(merged)

    st.download_button(
        "⬇️ Download Waste Recovery Report",
        data=merged.to_csv(index=False),
        file_name="waste_recovery_report.csv",
        mime="text/csv"
    )
