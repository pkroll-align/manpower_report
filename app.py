import streamlit as st
import gspread
import pandas as pd
import json
from google.oauth2.service_account import Credentials

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

SHEET_URL = "https://docs.google.com/spreadsheets/d/1ZRTbCI0b7q1OjEf5NOn-IZbVgmetqGkF0Koa4xxliI4"
WORKSHEET_NAME = "Day Form Responses"

sheet = gc.open_by_url(SHEET_URL).worksheet(WORKSHEET_NAME)

data = sheet.get_all_records()
df = pd.DataFrame(data)

st.title("Manpower Dashboard")
st.dataframe(df, use_container_width=True)
st.write("Rows loaded:", len(df))