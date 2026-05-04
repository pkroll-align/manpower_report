import streamlit as st
import gspread
import pandas as pd
import json
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Manpower Dashboard", layout="wide")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

service_account_info = json.loads(st.secrets["gcp_service_account"]["json"])

creds = Credentials.from_service_account_info(
    service_account_info,
    scopes=SCOPES
)

gc = gspread.authorize(creds)

SHEET_ID = "1e-0KRdTZQbQj4HAlJxerF7bHFp2kC3-vZuFIUaVnoGU"
WORKSHEET_NAME = "Day Form Responses"

st.write("Service account email being used:")
st.code(service_account_info["client_email"])

st.title("Manpower Dashboard")

spreadsheet = gc.open_by_key(SHEET_ID)

st.subheader("Available worksheets")
worksheet_names = [ws.title for ws in spreadsheet.worksheets()]
st.write(worksheet_names)

sheet = spreadsheet.worksheet(WORKSHEET_NAME)

data = sheet.get_all_records()
df = pd.DataFrame(data)

st.subheader("Raw Data")
st.dataframe(df, use_container_width=True)

st.write("Rows loaded:", len(df))
