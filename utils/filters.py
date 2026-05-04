import pandas as pd
import streamlit as st


def apply_filters(df):
    filtered_df = df.copy()

    st.sidebar.header("Filters")

    date_col = "Timestamp"
    company_col = "Company:"
    time_col = "Time"
    shift_col = "Which shift?"

    # Date filter
    if date_col in filtered_df.columns:
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

            if (
                isinstance(selected_date_range, tuple)
                and len(selected_date_range) == 2
            ):
                start_date, end_date = selected_date_range

                filtered_df = filtered_df[
                    (filtered_df[date_col].dt.date >= start_date)
                    & (filtered_df[date_col].dt.date <= end_date)
                ]

    # Shift filter
    if shift_col in filtered_df.columns:
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
    if time_col in filtered_df.columns:
        time_options = [
            "9:00 AM",
            "12:00 PM",
            "3:00 PM",
            "6:00 PM",
            "9:00 PM",
            "12:00 AM",
            "3:00 AM",
            "6:00 AM",
        ]

        available_times = [
            t for t in time_options
            if t in filtered_df[time_col].dropna().unique()
        ]

        selected_times = st.sidebar.multiselect(
            "Time",
            options=available_times,
            default=available_times
        )

        if selected_times:
            filtered_df = filtered_df[
                filtered_df[time_col].isin(selected_times)
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