import streamlit as st

from utils.calculations import build_report_sections


SECTION_COLORS = {
    "Total Manpower": "#1f4e78",
    "Warehouse": "#5b9bd5",
    "DH13": "#70ad47",
    "DH15": "#70ad47",
    "DH18": "#70ad47",
    "DH20": "#70ad47",
    "Supercore": "#8064a2",
}


def render_report_header(selected_filters):
    report_date = selected_filters.get("date")
    report_shift = selected_filters.get("shift")
    report_time = selected_filters.get("time")

    st.markdown("## Manpower Report")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Date",
            report_date.strftime("%m/%d/%Y") if report_date else ""
        )

    with col2:
        st.metric("Shift", report_shift)

    with col3:
        st.metric("Time", report_time)


def render_section_header(section_name):
    color = SECTION_COLORS.get(section_name, "#404040")

    st.markdown(
        f"""
        <div style="
            background-color: {color};
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 20px;
            font-weight: 700;
            margin-top: 24px;
            margin-bottom: 8px;
        ">
            {section_name}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_report_table(section_df):
    numeric_cols = [
        col for col in section_df.columns
        if col != "Category"
    ]

    styled_df = (
        section_df.style
        .format({col: "{:,.0f}" for col in numeric_cols})
        .set_properties(
            subset=["Category"],
            **{
                "text-align": "left",
                "font-weight": "500",
                "min-width": "300px",
            }
        )
        .set_properties(
            subset=numeric_cols,
            **{
                "text-align": "center",
                "min-width": "80px",
            }
        )
        .apply(
            lambda row: [
                "font-weight: bold; background-color: #d9d9d9;"
                if row["Category"] == "TOTAL"
                else ""
                for _ in row
            ],
            axis=1
        )
    )

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )


def render_dashboard(filtered_df, selected_filters):
    render_report_header(selected_filters)

    sections = build_report_sections(filtered_df)

    for section_name, section_df in sections.items():
        render_section_header(section_name)
        render_report_table(section_df)

    st.markdown("---")

    with st.expander("Debug - rows used in report"):
        st.write("Rows used:", len(filtered_df))

        debug_cols = [
            "Timestamp",
            "Adjusted Date",
            "Company:",
            "Which shift?",
            "Time",
        ]

        available_debug_cols = [
            col for col in debug_cols
            if col in filtered_df.columns
        ]

        st.dataframe(
            filtered_df[available_debug_cols],
            use_container_width=True,
            hide_index=True
        )

    with st.expander("Filtered raw data"):
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

    with st.expander("Column names"):
        st.write(list(filtered_df.columns))