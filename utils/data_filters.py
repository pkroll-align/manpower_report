import pandas as pd


DATE_COL = "Adjusted Date"
TIMESTAMP_COL = "Timestamp"
COMPANY_COL = "Company:"
TIME_COL = "Time"
SHIFT_COL = "Which shift?"


DAY_SHIFT_TIMES = [
    "9:00 AM",
    "12:00 PM",
    "3:00 PM",
    "6:00 PM",
]

NIGHT_SHIFT_TIMES = [
    "9:00 PM",
    "12:00 AM",
    "3:00 AM",
    "6:00 AM",
]


def normalize_text_columns(df):
    df = df.copy()

    for col in [COMPANY_COL, TIME_COL, SHIFT_COL]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df


def dedupe_latest_company_entries(df):
    required_cols = [
        TIMESTAMP_COL,
        COMPANY_COL,
        DATE_COL,
        SHIFT_COL,
        TIME_COL,
    ]

    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        return df

    df = df.copy()
    df = normalize_text_columns(df)

    df[TIMESTAMP_COL] = pd.to_datetime(
        df[TIMESTAMP_COL],
        errors="coerce"
    )

    df[DATE_COL] = pd.to_datetime(
        df[DATE_COL],
        errors="coerce"
    )

    df = df.dropna(subset=[
        TIMESTAMP_COL,
        DATE_COL,
    ])

    df = df.sort_values(
        by=TIMESTAMP_COL,
        ascending=False
    )

    df = df.drop_duplicates(
        subset=[
            COMPANY_COL,
            DATE_COL,
            SHIFT_COL,
            TIME_COL,
        ],
        keep="first"
    )

    return df


def apply_report_filters(df, selected_date, selected_shift, selected_time):
    filtered_df = dedupe_latest_company_entries(df)

    if DATE_COL in filtered_df.columns and selected_date:
        selected_date = pd.to_datetime(selected_date).date()

        filtered_df = filtered_df[
            filtered_df[DATE_COL].dt.date == selected_date
        ]

    if SHIFT_COL in filtered_df.columns and selected_shift:
        filtered_df = filtered_df[
            filtered_df[SHIFT_COL] == selected_shift
        ]

    if TIME_COL in filtered_df.columns and selected_time:
        filtered_df = filtered_df[
            filtered_df[TIME_COL] == selected_time
        ]

    return filtered_df