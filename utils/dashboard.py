import streamlit as st

from utils.calculations import build_report_sections


SECTION_HEADER_COLOR = "#1f4e78"


def render_report_header(selected_filters):
    report_date = selected_filters.get("date")
    report_shift = selected_filters.get("shift")
    report_time = selected_filters.get("time")

    st.markdown("### Manpower Report")

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
    st.markdown(
        f"""
        <div style="
            background-color: {SECTION_HEADER_COLOR};
            color: white;
            padding: 4px 8px;
            border-radius: 3px;
            font-size: 14px;
            font-weight: 700;
            margin-top: 14px;
            margin-bottom: 5px;
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
        .set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("font-size", "10px"),
                    ("font-weight", "700"),
                    ("text-align", "center"),
                    ("padding", "2px 4px"),
                    ("white-space", "normal"),
                ],
            },
            {
                "selector": "td",
                "props": [
                    ("font-size", "10px"),
                    ("padding", "2px 4px"),
                    ("line-height", "1.1"),
                ],
            },
        ])
        .set_properties(
            subset=["Category"],
            **{
                "text-align": "left",
                "font-weight": "500",
                "min-width": "230px",
                "max-width": "260px",
                "white-space": "normal",
            }
        )
        .set_properties(
            subset=numeric_cols,
            **{
                "text-align": "center",
                "min-width": "48px",
                "max-width": "60px",
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