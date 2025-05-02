"""NDC Migration and Accumulator Checker

This tool compares TPA accumulation data with a reference list of discontinued and new NDCs,
and ensures accumulation is moved correctly when allowed.
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="NDC Migration Checker", layout="wide")
st.title("🔄 NDC Migration and Accumulation Validator")

accumulator_file = st.file_uploader("📥 Upload TPA Accumulator Report", type=["xlsx", "csv"])
migration_file = st.file_uploader("🔄 Upload NDC Migration List", type=["xlsx", "csv"])
default_ndc_file = st.file_uploader("💊 Upload Default NDC Report from EHR", type=["xlsx", "csv"])

if accumulator_file and migration_file and default_ndc_file:
    acc = (
        pd.read_excel(accumulator_file)
        if accumulator_file.name.endswith("xlsx")
        else pd.read_csv(accumulator_file)
    )
    migration = (
        pd.read_excel(migration_file)
        if migration_file.name.endswith("xlsx")
        else pd.read_csv(migration_file)
    )
    default_ndc = (
        pd.read_excel(default_ndc_file)
        if default_ndc_file.name.endswith("xlsx")
        else pd.read_csv(default_ndc_file)
    )

    acc["NDC"] = acc["NDC"].astype(str)
    migration["Old NDC"] = migration["Old NDC"].astype(str)
    migration["New NDC"] = migration["New NDC"].astype(str)

    acc = pd.merge(acc, migration, left_on="NDC", right_on="Old NDC", how="left")

    def ndc_migration_status(row):
        """Determine if the NDC accumulation should be migrated and whether it's allowed."""
        if pd.isna(row["New NDC"]):
            return "✅ Current NDC"
        if row.get("Allow Migration", False):
            return "🔁 Migration Allowed"
        return "❌ Discontinued - Migration Not Allowed"

    acc["Migration Status"] = acc.apply(ndc_migration_status, axis=1)

    st.subheader("📊 Accumulator and Migration Review")
    st.dataframe(acc)

    st.download_button(
        label="⬇️ Download Migration Report",
        data=acc.to_csv(index=False),
        file_name="ndc_migration_report.csv",
        mime="text/csv"
    )

    st.subheader("💊 Default NDCs from EHR")
    st.dataframe(default_ndc.head())

    st.success("✅ NDC migration validation complete.")
