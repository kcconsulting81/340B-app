"""340B Medicaid Claims Validator

This module uploads Medicaid claims and a BIN/PCN/Group library, validates claim-level
340B billing status, modifiers, and plan carve-in policies, and flags potential 
duplicate discounts or billing rule violations.
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Medicaid Claims Validator", layout="wide")
st.title("🧾 340B Medicaid Claims Validator")

# Upload Medicaid claims and plan library
claims_file = st.file_uploader("💊 Upload Medicaid Claims File", type=["xlsx", "csv"])
bin_file = st.file_uploader("📚 Upload Medicaid BIN/PCN/Group Library", type=["xlsx", "csv"])

if claims_file and bin_file:
    # Read files into DataFrames
    claims_df = (
        pd.read_excel(claims_file)
        if claims_file.name.endswith("xlsx")
        else pd.read_csv(claims_file)
    )
    plans_df = (
        pd.read_excel(bin_file)
        if bin_file.name.endswith("xlsx")
        else pd.read_csv(bin_file)
    )

    st.subheader("💊 Claims Preview")
    st.dataframe(claims_df.head())

    st.subheader("📚 Plan Library Preview")
    st.dataframe(plans_df.head())

    # Normalize fields for consistent matching
    for col in ["BIN", "PCN", "Group"]:
        if col in plans_df.columns:
            plans_df[col] = plans_df[col].astype(str)
        if col in claims_df.columns:
            claims_df[col] = claims_df[col].astype(str)

    # Merge on BIN/PCN/Group to map each claim to a plan
    merged = pd.merge(
        claims_df,
        plans_df,
        on=["BIN", "PCN", "Group"],
        how="left",
        suffixes=("", "_plan")
    )

    def flag_issue(row):
        """Determine billing compliance based on claim and plan attributes."""
        if pd.isna(row.get("Plan Name", None)):
            return "❌ Unknown Plan (No 340B policy)"
        if row["Claim Type"].upper() == "FFS":
            if str(row.get("Modifier", "")).upper() not in ["UD", "U6"]:
                return "❌ FFS claim missing required 340B modifier"
        if row["Claim Type"].upper() == "MCO":
            if row.get("Allow 340B", True) is False:
                return "❌ MCO plan excludes 340B billing"
        return ""

    merged["Issue"] = merged.apply(flag_issue, axis=1)

    flagged = merged[merged["Issue"] != ""]

    st.subheader("🚨 Flagged Claims")
    st.dataframe(flagged)

    st.download_button(
        label="⬇️ Download Claim Issues",
        data=flagged.to_csv(index=False),
        file_name="medicaid_claim_issues.csv",
        mime="text/csv"
    )
# Completed
