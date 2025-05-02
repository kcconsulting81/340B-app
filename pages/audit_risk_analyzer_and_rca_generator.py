"""Audit Risk Analyzer and RCA Generator

Analyzes historical audit findings, compares them to current program data, and generates
risk scores, root cause analyses, and remediation plans.
"""

import pandas as pd
import streamlit as st

st.set_page_config(page_title="🛡️ Audit Risk Analyzer", layout="wide")
st.title("🛡️ Audit Risk Analyzer and RCA Generator")

st.markdown(
    "Upload historical HRSA or third-party audit findings. "
    "Compare to your current program data to identify areas at high risk for repeat findings."
)

# File uploads
findings_file = st.file_uploader(
    "📁 Upload Historical Audit Findings", type=["xlsx", "csv"]
)
current_data_file = st.file_uploader(
    "📥 Upload Current Program Snapshot (e.g., claims, OPAIS)", type=["xlsx", "csv"]
)

if findings_file and current_data_file:
    # Load files
    past = (
        pd.read_excel(findings_file)
        if findings_file.name.endswith("xlsx")
        else pd.read_csv(findings_file)
    )
    current = (
        pd.read_excel(current_data_file)
        if current_data_file.name.endswith("xlsx")
        else pd.read_csv(current_data_file)
    )

    st.subheader("📊 Risk Scoring and Analysis")
    if "Finding Type" in past.columns and "Area Affected" in past.columns:
        summary = past.groupby("Finding Type").size().reset_index(name="Frequency")
        summary["Risk %"] = (
            summary["Frequency"] / summary["Frequency"].sum()
        ) * 100
        st.dataframe(summary)

    if "Area" in current.columns:
        def assign_risk(area):
            """Assigns a risk category based on audit history matching the area."""
            if pd.isna(area):
                return "Low Risk"
            return next(
                (ft for ft in past["Area Affected"].unique() if ft in str(area)),
                "Low Risk"
            )
        current["Risk Category"] = current["Area"].map(assign_risk)

        current["Risk Score"] = current["Risk Category"].apply(
            lambda x: 90 if x != "Low Risk" else 10
        )

        st.markdown("**🔍 Current Risk Profile by Area**")
        st.dataframe(
            current[["Area", "Risk Category", "Risk Score"]].drop_duplicates()
        )

        st.subheader("🛠️ Root Cause and Remediation Suggestions")
        flagged = current[current["Risk Score"] > 50].copy()
        flagged["Root Cause"] = "Likely process gap or data mismatch"
        flagged["Suggested Fix"] = (
            "Review provider alignment, TPA logs, and 340B carve-in rules"
        )
        flagged["Owner"] = "Compliance Officer"
        flagged["Timeline"] = "30 days"
        st.dataframe(flagged)

        st.download_button(
            label="⬇️ Download RCA Report",
            data=flagged.to_csv(index=False),
            file_name="audit_risk_rca_report.csv",
            mime="text/csv"
        )
    else:
        st.warning(
            "❗ Could not find expected columns like 'Finding Type' or 'Area Affected'."
        )
else:
    st.info("Please upload both historical audit findings and current data.")
