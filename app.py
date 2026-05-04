import streamlit as st
from utils.sheets import load_sheet_data

st.set_page_config(page_title="Manpower Dashboard", layout="wide")

SHEET_ID = "1e-0KRdTZQbQj4HAlJxerF7bHFp2kC3-vZuFIUaVnoGU"
WORKSHEET_NAME = "Day Form Responses"

st.title("Manpower Dashboard")

df = load_sheet_data(SHEET_ID, WORKSHEET_NAME)

st.subheader("Raw Data")
st.dataframe(df, use_container_width=True)

st.write("Rows loaded:", len(df))