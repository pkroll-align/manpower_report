import streamlit as st
from utilities.sheets import load_sheet_data

st.set_page_config(page_title="Manpower Dashboard", layout="wide")

SHEET_ID = "1ZRTbCI0b7q1OjEf5NOn-IZbVgmetqGkF0Koa4xxliI4"
WORKSHEET_NAME = "Day Form Responses"

st.title("Manpower Dashboard")

df = load_sheet_data(SHEET_ID, WORKSHEET_NAME)

st.subheader("Raw Data")
st.dataframe(df, use_container_width=True)

st.write("Rows loaded:", len(df))