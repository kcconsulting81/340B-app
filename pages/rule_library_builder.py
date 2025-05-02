"""340B Rule Library Builder

This module allows users to upload and store reference rules such as orphan drug NDCs,
provider carve-in status, and Medicaid plan logic for ongoing 340B compliance validation.
"""

import pandas as pd
import streamlit as st

st.set_page_config(page_title="340B Rule Library", layout="wide")
st.title("📚 340B Compliance Rule Library Builder")

rule_file = st.file_uploader(
    "📤 Upload Rule File (Orphan NDCs, Carve-In Logic, Plan BINs)", type=["xlsx", "csv"]
)

if rule_file:
    rules = (
        pd.read_excel(rule_file)
        if rule_file.name.endswith("xlsx")
        else pd.read_csv(rule_file)
    )

    st.subheader("📖 Rule File Preview")
    st.dataframe(rules.head())

    st.download_button(
        label="⬇️ Download Stored Rule Library",
        data=rules.to_csv(index=False),
        file_name="340B_compliance_rules.csv",
        mime="text/csv"
    )

    st.success("✅ Rule library stored successfully.")
else:
    st.info("📁 Please upload a rule file to view or store compliance logic.")
