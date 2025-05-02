"""340B Monthly Compliance Screener

This module audits 340B compliance across all claims/dispenses by validating
provider eligibility, site registration, Medicaid carve-in status, and orphan drug rules.
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="340B Monthly Compliance Screener",
    layout="wide"
)
st.title("🛡️ 340B Full Compliance Review")

# Upload required reference files
dispense_file = st.file_uploader(
    "💊 Upload Dispense or Claim File",
    type=["xlsx", "csv"]
)
provider_file = st.file_uploader(
    "🧑‍⚕️ Upload Provider Eligibility List",
    type=["xlsx", "csv"]
)
site_file = st.file_uploader(
    "📍 Upload Registered Site List",
    type=["xlsx", "csv"]
)
orphan_file = st.file_uploader(
    "🧬 Upload Orphan Drug NDC List",
    type=["xlsx", "csv"]
)
mef_file = st.file_uploader(
    "🗂 Upload Medicaid Exclusion File (MEF)",
    type=["xlsx", "csv"]
)

# Proceed when all files are uploaded
if all([
    dispense_file,
    provider_file,
    site_file,
    orphan_file,
    mef_file
]):
    claims = pd.read_excel(dispense_file) if dispense_file.name.endswith("xlsx") else pd.read_csv(
        dispense_file
    )
    claims = (
        pd.read_excel(dispense_file)
        if dispense_file.name.endswith("xlsx")
        else pd.read_csv(dispense_file)
    )
    providers = (
        pd.read_excel(provider_file)
        if provider_file.name.endswith("xlsx")
        else pd.read_csv(provider_file)
    )
    sites = (
        pd.read_excel(site_file)
        if site_file.name.endswith("xlsx")
        else pd.read_csv(site_file)
    )
    orphans = (
        pd.read_excel(orphan_file)
        if orphan_file.name.endswith("xlsx")
        else pd.read_csv(orphan_file)
    )
    mef = (
        pd.read_excel(mef_file)
        if mef_file.name.endswith("xlsx")
        else pd.read_csv(mef_file)
    )

    orphans = pd.read_excel(orphan_file) if orphan_file.name.endswith("xlsx") else pd.read_csv(
        orphan_file
    )
    mef = pd.read_excel(mef_file) if mef_file.name.endswith("xlsx") else pd.read_csv(
        mef_file
    )

    # Normalize date fields
    claims["Date"] = pd.to_datetime(claims["Date"])
    providers["Start Date"] = pd.to_datetime(providers["Start Date"])
    providers["End Date"] = pd.to_datetime(providers["End Date"])

    # Merge all reference data into the claims
    merged = pd.merge(claims, providers, on="NPI", how="left")
    merged = pd.merge(merged, sites, on="Site", how="left")
    merged["Orphan"] = merged["NDC"].isin(orphans["NDC"])
    merged = pd.merge(merged, mef, on="NPI", how="left")

    def check_compliance(row):
        """Return a compliance flag based on all applicable 340B rules."""
        if pd.isna(row["Provider Name"]):
            return "❌ Invalid Provider"
        if row["Date"] < row["Start Date"] or (
            pd.notna(row["End Date"]) and row["Date"] > row["End Date"]
        ):
            return "❌ Provider Not Active"
        if pd.isna(row["Site Type"]):
            return "❌ Unregistered Site"
        if (
            row["Claim Type"] == "Medicaid"
            and row.get("Carve-In", True) is False
            and row.get("Billed 340B", False)
        ):
            return "❌ Duplicate Discount (Carved Out)"
        if row["Orphan"] and row.get("Entity Type", "") in ["PED", "CAN", "CAH"]:
            return "❌ Orphan Drug Restriction"
        return "✅ Compliant"

    merged["Compliance Status"] = merged.apply(check_compliance, axis=1)

    st.subheader("🧾 Compliance Screening Results")
    st.dataframe(
        merged[["NDC", "Site", "NPI", "Date", "Compliance Status"]]
    )

    violations = merged[merged["Compliance Status"] != "✅ Compliant"]

    st.subheader("🚨 Compliance Flags")
    st.dataframe(violations)

    st.download_button(
        label="⬇️ Download Compliance Report",
        data=violations.to_csv(index=False),
        file_name="monthly_compliance_violations.csv",
        mime="text/csv"
    )
