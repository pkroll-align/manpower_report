import json
import pandas as pd
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def get_credentials():
    service_account_info = json.loads(
        st.secrets["gcp_service_account"]["json"]
    )

    return Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPES
    )


def get_google_client():
    creds = get_credentials()
    return gspread.authorize(creds)


def clean_headers(headers):
    clean_headers_list = []
    seen = {}

    for h in headers:
        h = h.strip() if h else "Column"

        if h in seen:
            seen[h] += 1
            h = f"{h}_{seen[h]}"
        else:
            seen[h] = 0

        clean_headers_list.append(h)

    return clean_headers_list


def normalize_rows(rows, header_count):
    normalized_rows = []

    for row in rows:
        if len(row) < header_count:
            row = row + [""] * (header_count - len(row))
        elif len(row) > header_count:
            row = row[:header_count]

        normalized_rows.append(row)

    return normalized_rows


def load_sheet_data(sheet_id, worksheet_name, range_name="A:BT"):
    gc = get_google_client()

    spreadsheet = gspread.Spreadsheet(gc.http_client, {"id": sheet_id})
    sheet = spreadsheet.worksheet(worksheet_name)

    values = sheet.get(range_name)

    if not values:
        return pd.DataFrame()

    headers = clean_headers(values[0])
    rows = values[1:]

    rows = normalize_rows(rows, len(headers))

    df = pd.DataFrame(rows, columns=headers)

    # Drop unwanted source columns: E, AO, AP
    columns_to_drop = []

    for index in [4, 40, 41]:
        if index < len(df.columns):
            columns_to_drop.append(df.columns[index])

    df = df.drop(columns=columns_to_drop)

    return df