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
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 15px;
            font-weight: 700;
            margin-top: 16px;
            margin-bottom: 6px;
        ">
            {section_name}
        </div>
        """,
        unsafe_allow_html=True
    )


def style_report_table(section_df, is_total=False):
    numeric_cols = [
        col for col in section_df.columns
        if col != "Category"
    ]

    base_styles = [
        {
            "selector": "th",
            "props": [
                ("font-size", "12px"),
                ("font-weight", "700"),
                ("text-align", "center"),
                ("padding", "3px 6px"),
            ],
        },
        {
            "selector": "td",
            "props": [
                ("font-size", "12px"),
                ("padding", "3px 6px"),
            ],
        },
    ]

    styled_df = (
        section_df.style
        .format({col: "{:,.0f}" for col in numeric_cols})
        .set_table_styles(base_styles)
        .set_properties(
            subset=["Category"],
            **{
                "text-align": "left",
                "font-weight": "700" if is_total else "500",
                "min-width": "260px",
            }
        )
        .set_properties(
            subset=numeric_cols,
            **{
                "text-align": "center",
                "font-weight": "700" if is_total else "400",
                "min-width": "65px",
            }
        )
    )

    if is_total:
        styled_df = styled_df.apply(
            lambda row: [
                "font-weight: bold; background-color: #d9d9d9;"
                for _ in row
            ],
            axis=1
        )

    return styled_df


def render_report_table(section_df):
    normal_rows = section_df[section_df["Category"] != "TOTAL"].copy()
    total_row = section_df[section_df["Category"] == "TOTAL"].copy()

    st.dataframe(
        style_report_table(normal_rows),
        use_container_width=True,
        hide_index=True
    )

    if not total_row.empty:
        st.dataframe(
            style_report_table(total_row, is_total=True),
            use_container_width=True,
            hide_index=True
        )


def render_dashboard(filtered_df, selected_filters):
    render_report_header(selected_filters)

    sections = build_report_sections(filtered_df)

    for section_name, section_df in sections.items():
        render_section_header(section_name)
        render_report_table(section_df)