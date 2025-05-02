"""Audit Request Response Generator

Allows upload of HRSA audit request template and auto-populates data for a selected
Parent Covered Entity (CE) from internal data sources like providers, contracts, and sites.
"""

import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="📑 HRSA Audit Response Generator", layout="wide")
st.title("📑 HRSA Audit Request Response Generator")

st.markdown("Upload the HRSA or 3rd-party audit request template and generate a completed "
            "response by selecting a Parent Covered Entity and linking stored data.")

# Upload audit request template
template_file = st.file_uploader("📥 Upload Audit Request Template (Excel)", type=["xlsx"])
parent_ce = st.selectbox("🏥 Select Parent Covered Entity", [
    "CE001 - University Health",
    "CE002 - Regional Hospital",
    "CE003 - Community Clinic"
])

# Load stored data files (example placeholders)
provider_file = os.path.join("library", "provider_list.csv")
contract_file = os.path.join("library", "contract_pharmacies.csv")
claim_file = os.path.join("library", "compliance_flags.csv")
site_file = os.path.join("library", "340B_site_crosswalk.csv")

def load_file(path):
    """Loads a CSV file from the library folder if available."""
    return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()

providers = load_file(provider_file)
contracts = load_file(contract_file)
claims = load_file(claim_file)
sites = load_file(site_file)

if template_file:
    try:
        writer = pd.ExcelWriter("audit_response.xlsx", engine="xlsxwriter")

        # Fill template with matching data (mock tab structure)
        if not providers.empty:
            providers.to_excel(writer, sheet_name="Providers", index=False)
        if not claims.empty:
            claims.to_excel(writer, sheet_name="Claims", index=False)
        if not contracts.empty:
            contracts.to_excel(writer, sheet_name="Contracts", index=False)
        if not sites.empty:
            sites.to_excel(writer, sheet_name="Sites", index=False)

        writer.close()

        with open("audit_response.xlsx", "rb") as f:
            st.download_button(
                label="⬇️ Download Completed Audit Response",
                data=f,
                file_name=f"HRSA_Audit_Response_{parent_ce.replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        st.success("✅ Audit response file generated and ready for download.")
    except (ValueError, IOError, KeyError) as e:
        st.error(f"❌ Error generating file: {e}")
else:
    st.info("Upload an Excel audit request template to begin.")
