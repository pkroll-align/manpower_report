import streamlit as st

from utils.sheets import load_sheet_data
from utils.filters import apply_filters
from utils.dashboard import render_dashboard

st.set_page_config(page_title="Manpower Dashboard", layout="wide")

SHEET_ID = "1ZRTbCI0b7q1OjEf5NOn-IZbVgmetqGkF0Koa4xxliI4"
WORKSHEET_NAME = "Day Form Responses"

st.title("Manpower Dashboard")

df = load_sheet_data(SHEET_ID, WORKSHEET_NAME)
filtered_df = apply_filters(df)

render_dashboard(filtered_df)