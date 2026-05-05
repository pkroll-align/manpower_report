import json
import os
import time

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials


SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

CACHE_TTL_SECONDS = 120

_cached_df = None
_cached_at = 0


def get_credentials():
    service_account_json = os.environ.get("GCP_SERVICE_ACCOUNT_JSON")

    if not service_account_json:
        raise RuntimeError("Missing GCP_SERVICE_ACCOUNT_JSON environment variable.")

    service_account_info = json.loads(service_account_json)

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


def fetch_sheet_data(sheet_id, worksheet_name, range_name="A:BU"):
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

    return df


def load_sheet_data(sheet_id, worksheet_name, range_name="A:BU", force_refresh=False):
    global _cached_df
    global _cached_at

    now = time.time()

    cache_is_valid = (
        _cached_df is not None
        and not force_refresh
        and now - _cached_at < CACHE_TTL_SECONDS
    )

    if cache_is_valid:
        return _cached_df.copy()

    df = fetch_sheet_data(sheet_id, worksheet_name, range_name)

    _cached_df = df.copy()
    _cached_at = now

    return df