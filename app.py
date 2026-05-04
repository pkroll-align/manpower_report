import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Manpower Dashboard", layout="wide")

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

gc = gspread.authorize(creds)

SHEET_URL = "https://docs.google.com/spreadsheets/d/1ZRTbCI0b7q1OjEf5NOn-IZbVgmetqGkF0Koa4xxliI4"
WORKSHEET_NAME = "Day Form Responses"

sheet = gc.open_by_url(SHEET_URL).worksheet(WORKSHEET_NAME)

data = sheet.get_all_records()
df = pd.DataFrame(data)

st.title("Manpower Dashboard")

st.subheader("Raw Data")
st.dataframe(df, use_container_width=True)

st.write("Rows loaded:", len(df))