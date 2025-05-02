"""Manufacturer Restrictions Manager

Manages state-specific manufacturer 340B restrictions and links restricted NDCs to
approved therapeutic or biosimilar alternatives. Also tracks markup logic for cost modeling.
"""

import pandas as pd
import streamlit as st

st.set_page_config(page_title="🚫 Manufacturer Restrictions Manager", layout="wide")
st.title("🚫 Manufacturer Restrictions Manager")

st.markdown("Upload and manage manufacturer-restricted NDCs, view crosswalks to alternative drugs, "
            "and maintain markup formulas for cost projections.")

# Upload restriction and crosswalk files
restrictions_file = st.file_uploader("📥 Upload Manufacturer Restrictions List", type=["csv", "xlsx"])
alternatives_file = st.file_uploader("🔄 Upload NDC Alternative Crosswalk", type=["csv", "xlsx"])
markup_file = st.file_uploader("💰 Upload Markup Algorithm Table", type=["csv", "xlsx"])

# Load data
def load_uploaded(file):
    if not file:
        return pd.DataFrame()
    if file.name.endswith("xlsx"):
        return pd.read_excel(file)
    return pd.read_csv(file)

restrictions_df = load_uploaded(restrictions_file)
alternatives_df = load_uploaded(alternatives_file)
markup_df = load_uploaded(markup_file)

# Display manufacturer restrictions
if not restrictions_df.empty:
    st.subheader("📛 Manufacturer Restrictions by State")
    st.dataframe(restrictions_df)

# Display alternatives
if not alternatives_df.empty:
    st.subheader("💊 Therapeutic/Biosimilar Alternatives")
    st.dataframe(alternatives_df)

# Display markup rules
if not markup_df.empty:
    st.subheader("📈 Markup Algorithms")
    st.dataframe(markup_df)

    # Optional: basic ROI estimate per NDC if data exists
    if "NDC" in markup_df.columns and "Markup %" in markup_df.columns:
        st.subheader("📊 ROI Model Preview (Assuming $100 Base Price)")
        markup_df["Projected Price"] = 100 * (1 + markup_df["Markup %"] / 100)
        st.dataframe(markup_df[["NDC", "Markup %", "Projected Price"]])

# Download
if not restrictions_df.empty:
    st.download_button(
        label="⬇️ Download Restriction Table",
        data=restrictions_df.to_csv(index=False),
        file_name="restricted_ndcs.csv",
        mime="text/csv"
    )
