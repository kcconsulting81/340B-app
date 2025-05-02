"""340B Medicare Cost Report Parser

This app allows users to upload a Medicare Cost Report (MCR) Excel file and identify
outpatient cost centers that may be eligible for 340B registration based on
Worksheet A, C, and E Part A.
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="340B MCR Parser", layout="wide")
st.title("📊 340B Medicare Cost Report Parser")

uploaded_file = st.file_uploader(
    "Upload Medicare Cost Report (Excel)", type=["xlsx"]
)

if uploaded_file:
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names

        st.success("✅ File loaded successfully")
        st.write("Worksheets found:", sheet_names)

        ws_a = xls.parse("Worksheet A")
        ws_c = xls.parse("Worksheet C")
        ws_e = xls.parse("Worksheet E Part A")

        st.subheader("📉 DSH % from Worksheet E Part A")
        try:
            dsh_percent = ws_e.iloc[32]
            st.dataframe(dsh_percent)
        except IndexError:
            st.warning("⚠️ Could not locate DSH % on expected line (Line 33).")

        st.subheader("🏥 Outpatient Cost Centers with Revenue > $0")

        if "Cost Center" in ws_a.columns and "Cost Center" in ws_c.columns:
            merged = pd.merge(ws_a, ws_c, on="Cost Center", how="inner")

            revenue_col = [
                col for col in merged.columns if "revenue" in col.lower()
            ]
            if revenue_col:
                rev_col = revenue_col[0]
                eligible_sites = merged[merged[rev_col] > 0]
                st.dataframe(eligible_sites)

                st.download_button(
                    label="⬇️ Download Eligible Site Crosswalk (CSV)",
                    data=eligible_sites.to_csv(index=False),
                    file_name="340B_site_crosswalk.csv",
                    mime="text/csv"
                )
            else:
                st.warning("⚠️ Could not identify outpatient revenue column.")
        else:
            st.error("❌ Missing 'Cost Center' column in either Worksheet A or C.")

    except pd.errors.ParserError as pe:
        st.error(f"❌ Parsing error in Excel file: {pe}")
    except ValueError as ve:
        st.error(f"❌ Excel Parsing Error: {ve}")
    except FileNotFoundError as fnfe:
        st.error(f"❌ File not found: {fnfe}")
    except KeyError as ke:
        st.error(f"❌ Missing key in data: {ke}")
    except (IOError, AttributeError) as e:
        st.error(f"❌ An unexpected error occurred: {type(e).__name__} – {e}")
