import pandas as pd
import streamlit as st
from datetime import date


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


def apply_filters(df):
    filtered_df = df.copy()

    st.sidebar.header("Filters")

    date_col = "Timestamp"
    company_col = "Company:"
    time_col = "Time"
    shift_col = "Which shift?"

    # Date filter: single day, default today
    if date_col in filtered_df.columns:
        filtered_df[date_col] = pd.to_datetime(
            filtered_df[date_col],
            errors="coerce"
        )

        selected_date = st.sidebar.date_input(
            "Date",
            value=date.today()
        )

        filtered_df = filtered_df[
            filtered_df[date_col].dt.date == selected_date
        ]

    # Shift dropdown
    selected_shift = st.sidebar.selectbox(
        "Shift",
        options=["Day Shift", "Night Shift"]
    )

    if shift_col in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df[shift_col] == selected_shift
        ]

    # Time dropdown changes based on selected shift
    if selected_shift == "Day Shift":
        time_options = DAY_SHIFT_TIMES
    else:
        time_options = NIGHT_SHIFT_TIMES

    selected_time = st.sidebar.selectbox(
        "Time",
        options=time_options
    )

    if time_col in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df[time_col] == selected_time
        ]

    # Company filter
    if company_col in filtered_df.columns:
        company_options = sorted([
            x for x in filtered_df[company_col].dropna().unique()
            if str(x).strip() != ""
        ])

        selected_companies = st.sidebar.multiselect(
            "Company",
            options=company_options,
            default=company_options
        )

        if selected_companies:
            filtered_df = filtered_df[
                filtered_df[company_col].isin(selected_companies)
            ]

    return filtered_df