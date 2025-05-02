"""Provider-Site Eligibility Checker

This module cross-references a provider's practice location and NPI
against 340B-registered sites to verify eligibility alignment.
"""

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Provider-Site Eligibility Checker", layout="wide")
st.title("👩‍⚕️ Provider and Site Eligibility Validator")

provider_file = st.file_uploader("👨‍⚕️ Upload Provider List (with NPI)", type=["xlsx", "csv"])
site_file = st.file_uploader("🏥 Upload 340B Site Registration List", type=["xlsx", "csv"])

if provider_file and site_file:
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

    providers["NPI"] = providers["NPI"].astype(str)
    sites["NPI"] = sites["NPI"].astype(str)

    merged = pd.merge(providers, sites, on="NPI", how="left")

    unmatched = merged[merged["Site Name"].isna()]

    st.subheader("📍 Providers NOT aligned to any 340B-registered site")
    st.dataframe(unmatched)

    st.download_button(
        label="⬇️ Download Unmatched Providers",
        data=unmatched.to_csv(index=False),
        file_name="provider_site_unmatched.csv",
        mime="text/csv"
    )

    st.success("✅ Provider-site eligibility validation complete.")
