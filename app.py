import streamlit as st
import gspread
import pandas as pd
import json
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Manpower Dashboard", layout="wide")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]

service_account_info = json.loads(st.secrets["gcp_service_account"]["json"])

creds = Credentials.from_service_account_info(
    service_account_info,
    scopes=SCOPES
)

gc = gspread.authorize(creds)

SHEET_ID = "1e-0KRdTZQbQj4HAlJxerF7bHFp2kC3-vZuFIUaVnoGU"
WORKSHEET_NAME = "Day Form Responses"

st.title("Manpower Dashboard")

spreadsheet = gspread.Spreadsheet(gc.http_client, {"id": SHEET_ID})
sheet = spreadsheet.worksheet(WORKSHEET_NAME)

sheet = spreadsheet.worksheet(WORKSHEET_NAME)

values = sheet.get_all_values()

headers = values[0]
rows = values[1:]

df = pd.DataFrame(rows, columns=headers)

st.subheader("Raw Data")
st.dataframe(df, use_container_width=True)

st.write("Rows loaded:", len(df))
