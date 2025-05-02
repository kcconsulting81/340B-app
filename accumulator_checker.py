import streamlit as st
import pandas as pd

st.set_page_config(page_title="Accumulator Checker", layout="wide")
st.title("🧬 340B Accumulator & Claims Validator")

# Upload files
accum_file = st.file_uploader("📦 Upload TPA Accumulator File", type=["xlsx", "csv"])
claims_file = st.file_uploader("💊 Upload Claims or Dispenses File", type=["xlsx", "csv"])

if accum_file and claims_file:
    # Load files
    acc_df = pd.read_excel(accum_file) if accum_file.name.endswith("xlsx") else pd.read_csv(accum_file)
    claims_df = pd.read_excel(claims_file) if claims_file.name.endswith("xlsx") else pd.read_csv(claims_file)

    st.subheader("📦 Accumulator Preview")
    st.dataframe(acc_df.head())

    st.subheader("💊 Claims Preview")
    st.dataframe(claims_df.head())

    # Normalize dates
    acc_df["Date"] = pd.to_datetime(acc_df["Date"])
    claims_df["Date"] = pd.to_datetime(claims_df["Date"])

    # Merge on NDC and Date
    merged = pd.merge(claims_df, acc_df, on=["NDC", "Date"], how="left", suffixes=("_claim", "_accum"))

    # Check accumulation presence
    merged["Accumulated"] = merged["Account Type_accum"].notna()

    # Flag logic
    def determine_issue(row):
        if row["Billed 340B"] and not row["Accumulated"]:
            return "❌ Claimed as 340B but not accumulated (Duplicate Risk)"
        elif not row["Billed 340B"] and row["Accumulated"]:
            return "⚠️ Accumulated but not billed as 340B (Lost Savings)"
        else:
            return ""

    if "Billed 340B" in merged.columns:
        merged["Issue"] = merged.apply(determine_issue, axis=1)
    else:
        merged["Issue"] = merged["Accumulated"].apply(lambda x: "" if x else "❌ No accumulation found")

    # Filter only issues
    flagged = merged[merged["Issue"] != ""]

    st.subheader("🚨 Flagged Issues")
    st.dataframe(flagged)

    st.download_button("⬇️ Download Issue Report",
                       flagged.to_csv(index=False),
                       file_name="accumulator_issues.csv",
                       mime="text/csv")
