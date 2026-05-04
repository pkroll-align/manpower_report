import streamlit as st
import gspread
import pandas as pd
import json
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Manpower Dashboard", layout="wide")

# --- Scopes ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

# --- Load credentials from Streamlit secrets ---
service_account_info = json.loads(st.secrets["gcp_service_account"]["json"])

creds = Credentials.from_service_account_info(
    service_account_info,
    scopes=SCOPES
)

gc = gspread.authorize(creds)

# --- Your Sheet Info ---
SHEET_ID = "1e-0KRdTZQbQj4HAlJxerF7bHFp2kC3-vZuFIUaVnoGU"
WORKSHEET_NAME = "Day Form Responses"

# --- Load data ---
sheet = gc.open_by_key(SHEET_ID).worksheet(WORKSHEET_NAME)
data = sheet.get_all_records()
df = pd.DataFrame(data)

# --- UI ---
st.title("Manpower Dashboard")

st.subheader("Raw Data")
st.dataframe(df, use_container_width=True)

st.write("Rows loaded:", len(df))