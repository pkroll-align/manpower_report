import streamlit as st

from utils.calculations import build_report_sections


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
                "min-width": "280px",
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


def render_section(section_name, section_df):
    st.markdown("---")
    st.markdown(f"### {section_name}")
    render_report_table(section_df)


def render_dashboard(filtered_df, selected_filters):
    render_report_header(selected_filters)

    sections = build_report_sections(filtered_df)

    for section_name, section_df in sections.items():
        render_section(section_name, section_df)

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