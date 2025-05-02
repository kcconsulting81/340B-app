"""340B Report Generator

Generates on-demand summary reports from available uploaded or generated files, including
compliance flags, overcharge summaries, and monthly report insights.
"""

import os

import pandas as pd
import streamlit as st

st.set_page_config(page_title="📊 Report Generator", layout="wide")
st.title("📊 340B Report Generator")

st.markdown(
    "This tool consolidates reports from your document library and generated outputs "
    "to give you a monthly or flagged snapshot of 340B compliance and activity."
)

# Set paths
LIBRARY_FOLDER = "library"
SUMMARY_DATA = {
    "Compliance Flags": "compliance_flags.csv",
    "Overcharges": "invoice_overcharges.csv",
    "Eligible Sites": "340B_site_crosswalk.csv",
    "Document Log": "library_index.csv"
}

# Select report type
st.subheader("📁 Select Report Type")
report_type = st.selectbox("Choose a report to view", list(SUMMARY_DATA.keys()))

report_path = os.path.join(LIBRARY_FOLDER, SUMMARY_DATA[report_type])

if os.path.exists(report_path):
    df = pd.read_csv(report_path)

    st.success(f"✅ Loaded report: {report_type}")
    st.dataframe(df)

    st.download_button(
        f"⬇️ Download {report_type} Report",
        data=df.to_csv(index=False),
        file_name=f"{report_type.replace(' ', '_').lower()}_report.csv",
        mime="text/csv"
    )
else:
    st.warning(f"⚠️ The selected report '{report_type}' is not yet available in your library.")
