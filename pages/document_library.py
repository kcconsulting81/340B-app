"""Document Library Manager

Allows users to upload, categorize, store, and view a searchable list of historical documents
such as pricing files, cost reports, contracts, and invoice exports.
"""

import os
from datetime import datetime

import pandas as pd
import streamlit as st

# Constants should be uppercase
LIBRARY_FOLDER = "library"
os.makedirs(LIBRARY_FOLDER, exist_ok=True)

INDEX_FILE = os.path.join(LIBRARY_FOLDER, "library_index.csv")

# Load or create the index log
if os.path.exists(INDEX_FILE):
    index_df = pd.read_csv(INDEX_FILE)
else:
    index_df = pd.DataFrame(columns=["Filename", "Category", "Upload Date", "Path"])

st.set_page_config(page_title="📂 Document Library", layout="wide")
st.title("📂 340B Document Library")

st.subheader("📤 Upload Document")

uploaded_file = st.file_uploader(
    "Select a file to upload", type=["xlsx", "csv", "xls", "pdf"]
)
category = st.selectbox(  # type: ignore[attr-defined]
    "📁 Choose a category",
    [
        "Medicare Cost Report", "Ceiling Price File", "Wholesaler Pricing", "Invoice",
        "TPA Export", "Contract", "MEF", "OPAIS", "Other"
    ]
)

if uploaded_file and category:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    SAVE_NAME = f"{timestamp}_{uploaded_file.name}"
    save_path = os.path.join(LIBRARY_FOLDER, SAVE_NAME)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())  # type: ignore[attr-defined]

    new_entry = {
        "Filename": uploaded_file.name,
        "Category": category,
        "Upload Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Path": save_path
    }
    index_df = pd.concat([index_df, pd.DataFrame([new_entry])], ignore_index=True)
    index_df.to_csv(INDEX_FILE, index=False)

    st.success(f"✅ File '{uploaded_file.name}' uploaded and stored under '{category}'.")

st.subheader("📚 Stored Documents")
st.dataframe(index_df)

st.download_button(
    "⬇️ Download Document Log",
    data=index_df.to_csv(index=False),
    file_name="document_library_log.csv",
    mime="text/csv"
)
