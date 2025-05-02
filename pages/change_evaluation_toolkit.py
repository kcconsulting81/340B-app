"""Change Evaluation Toolkit

Allows submission of proposed program changes (e.g., new contracts, providers, drugs)
and generates a cost-benefit summary, risk score, and implementation plan.
"""

import os
import pandas as pd
import streamlit as st
from datetime import date

st.set_page_config(page_title="📝 Change Evaluation Toolkit", layout="wide")
st.title("📝 Change Evaluation Toolkit")

st.markdown("Submit and evaluate proposed changes to your 340B program including provider, drug, contract, or operational changes. "
            "This tool will calculate estimated ROI, risk level, and build a timeline for implementation.")

# Load prior submissions if exist
data_path = "library"
log_file = os.path.join(data_path, "change_evaluation_log.csv")
if os.path.exists(log_file):
    change_log = pd.read_csv(log_file)
else:
    change_log = pd.DataFrame(columns=[
        "Change Type", "Description", "Go-Live Date", "Estimated Cost ($)", "Estimated Savings ($)",
        "Risk Level", "ROI (%)", "Implementation Time (days)", "Submitted By", "Date Submitted"
    ])

# Form submission
st.subheader("📤 Submit New Change Request")

with st.form("change_form"):
    change_type = st.selectbox("Change Type", [
        "New Drug", "Provider Addition", "Contract Update", "Site Carve-In/Out", "TPA/Vendor Change", "Policy Revision"
    ])
    description = st.text_area("Brief Description of the Change")
    go_live = st.date_input("Planned Go-Live Date", value=date.today())
    cost = st.number_input("Estimated Implementation Cost ($)", min_value=0.0, value=0.0, step=100.0)
    savings = st.number_input("Estimated Financial Benefit ($ per year)", min_value=0.0, value=0.0, step=100.0)
    risk_level = st.selectbox("Compliance/Operational Risk Level", ["Low", "Medium", "High"])
    submitted_by = st.text_input("Submitted By")

    submit = st.form_submit_button("Evaluate and Submit")

if submit:
    roi = round(((savings - cost) / cost) * 100 if cost > 0 else 100, 2)
    days_to_implement = (go_live - date.today()).days

    new_row = pd.DataFrame([{
        "Change Type": change_type,
        "Description": description,
        "Go-Live Date": go_live,
        "Estimated Cost ($)": cost,
        "Estimated Savings ($)": savings,
        "Risk Level": risk_level,
        "ROI (%)": roi,
        "Implementation Time (days)": days_to_implement,
        "Submitted By": submitted_by,
        "Date Submitted": date.today()
    }])
    change_log = pd.concat([change_log, new_row], ignore_index=True)
    change_log.to_csv(log_file, index=False)
    st.success("✅ Change evaluation submitted and logged.")

# Show all evaluations
st.subheader("📋 Logged Change Evaluations")
st.dataframe(change_log)

st.download_button(
    "⬇️ Download Evaluation Log",
    data=change_log.to_csv(index=False),
    file_name="change_evaluation_log.csv",
    mime="text/csv"
)
