"""Lookback Impact Modeler

Allows adjustment of patient definition rules (lookback windows) to simulate how eligibility
and financial performance change with different configurations.
"""

import pandas as pd
import streamlit as st
from datetime import timedelta

st.set_page_config(page_title="🕒 Lookback Impact Modeler", layout="wide")
st.title("🕒 Lookback Impact Modeler")

st.markdown(
    "Upload EPIC or encounter-based data including dispense dates and visit dates. "
    "Adjust the patient eligibility window (lookback before/after) to see how it affects "
    "340B qualification and savings."
)

# Upload files
dispense_file = st.file_uploader("📄 Upload Dispensed Drug File", type=["xlsx", "csv"])
visit_file = st.file_uploader("🩺 Upload Encounter Visit File", type=["xlsx", "csv"])

before_days = st.slider("⬅️ Lookback Days BEFORE Dispense", min_value=0, max_value=30, value=4)
after_days = st.slider("➡️ Lookback Days AFTER Dispense", min_value=0, max_value=30, value=4)

if dispense_file and visit_file:
    disp = (
        pd.read_excel(dispense_file)
        if dispense_file.name.endswith("xlsx")
        else pd.read_csv(dispense_file)
    )
    visits = (
        pd.read_excel(visit_file)
        if visit_file.name.endswith("xlsx")
        else pd.read_csv(visit_file)
    )

    # Expected columns
    disp["Dispense Date"] = pd.to_datetime(disp["Dispense Date"])
    visits["Visit Date"] = pd.to_datetime(visits["Visit Date"])

    merged = disp.merge(visits, on="Patient ID", suffixes=("_disp", "_visit"))

    def is_eligible(row):
        """Returns True if visit is within the lookback window around the dispense date."""
        start = row["Dispense Date"] - timedelta(days=before_days)
        end = row["Dispense Date"] + timedelta(days=after_days)
        return start <= row["Visit Date"] <= end

    merged["Eligible"] = merged.apply(is_eligible, axis=1)

    eligible = merged[merged["Eligible"]].sort_values("Visit Date", ascending=False)
    eligible = eligible.drop_duplicates(subset=["Dispense ID"])

    if "Unit Price ($)" in disp.columns and "Quantity" in disp.columns:
        disp["Qualified"] = disp["Dispense ID"].isin(eligible["Dispense ID"])
        disp["Potential Savings"] = disp["Quantity"] * disp["Unit Price ($)"]
        impact = disp.groupby("Qualified")["Potential Savings"].sum().reset_index()
        st.subheader("💰 Financial Impact Summary")
        st.dataframe(impact)

    st.subheader("📋 Eligible Dispenses Based on Current Lookback")
    st.dataframe(eligible)

    st.download_button(
        label="⬇️ Download Eligible Dispense Report",
        data=eligible.to_csv(index=False),
        file_name="lookback_eligible_dispenses.csv",
        mime="text/csv"
    )
else:
    st.info("Upload both the dispense file and encounter file to proceed.")
