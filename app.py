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

SHEET_ID = "1ZRTbCI0b7q1OjEf5NOn-IZbVgmetqGkF0Koa4xxliI4"
WORKSHEET_NAME = "Day Form Responses"

st.title("Manpower Dashboard")

spreadsheet = gspread.Spreadsheet(gc.http_client, {"id": SHEET_ID})
sheet = spreadsheet.worksheet(WORKSHEET_NAME)

data = sheet.get_all_records()
df = pd.DataFrame(data)

st.subheader("Raw Data")
st.dataframe(df, use_container_width=True)

st.write("Rows loaded:", len(df))
