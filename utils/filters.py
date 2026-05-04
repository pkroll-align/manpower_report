import pandas as pd
import streamlit as st


def find_column(df, possible_names):
    normalized_columns = {
        str(col).lower().strip(): col
        for col in df.columns
    }

    for name in possible_names:
        key = name.lower().strip()
        if key in normalized_columns:
            return normalized_columns[key]

    return None


def apply_filters(df):
    filtered_df = df.copy()

    st.sidebar.header("Filters")

    date_col = find_column(df, [
        "Timestamp",
        "Date",
        "Adjusted Date",
        "What date are you logging?"
    ])

    shift_col = find_column(df, [
        "Shift",
        "What shift are you logging?",
        "Day Shift",
        "Night Shift"
    ])

    time_col = find_column(df, [
        "Time",
        "Time_1",
        "What time are you logging?"
    ])

    # Date filter
    if date_col:
        filtered_df[date_col] = pd.to_datetime(
            filtered_df[date_col],
            errors="coerce"
        )

        valid_dates = filtered_df[date_col].dropna()

        if not valid_dates.empty:
            min_date = valid_dates.min().date()
            max_date = valid_dates.max().date()

            selected_date_range = st.sidebar.date_input(
                "Date range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )

            if isinstance(selected_date_range, tuple) and len(selected_date_range) == 2:
                start_date, end_date = selected_date_range

                filtered_df = filtered_df[
                    (filtered_df[date_col].dt.date >= start_date) &
                    (filtered_df[date_col].dt.date <= end_date)
                ]

    # Shift filter
    if shift_col:
        shift_options = sorted([
            x for x in filtered_df[shift_col].dropna().unique()
            if str(x).strip() != ""
        ])

        selected_shifts = st.sidebar.multiselect(
            "Shift",
            options=shift_options,
            default=shift_options
        )

        if selected_shifts:
            filtered_df = filtered_df[
                filtered_df[shift_col].isin(selected_shifts)
            ]

    # Time filter
    if time_col:
        time_options = sorted([
            x for x in filtered_df[time_col].dropna().unique()
            if str(x).strip() != ""
        ])

        selected_times = st.sidebar.multiselect(
            "Time",
            options=time_options,
            default=time_options
        )

        if selected_times:
            filtered_df = filtered_df[
                filtered_df[time_col].isin(selected_times)
            ]

    return filtered_df