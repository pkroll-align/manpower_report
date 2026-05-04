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

# --- Only pull A:BV ---
values = sheet.get("A:BV")

headers = values[0]
rows = values[1:]

# --- Clean duplicate / blank headers ---
clean_headers = []
seen = {}

for h in headers:
    h = h.strip() if h else "Column"

    if h in seen:
        seen[h] += 1
        new_h = f"{h}_{seen[h]}"
    else:
        seen[h] = 0
        new_h = h

    clean_headers.append(new_h)

df = pd.DataFrame(rows, columns=clean_headers)

st.subheader("Column Headers")
st.write(clean_headers)

st.subheader("Raw Data")
st.dataframe(df, use_container_width=True)

st.write("Rows loaded:", len(df))
