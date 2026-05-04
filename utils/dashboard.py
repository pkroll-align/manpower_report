import html

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
            {html.escape(section_name)}
        </div>
        """,
        unsafe_allow_html=True
    )


def format_cell_value(value, is_category=False):
    if is_category:
        return html.escape(str(value))

    try:
        return f"{float(value):,.0f}"
    except (TypeError, ValueError):
        return ""


def render_static_report_table(section_df):
    columns = list(section_df.columns)

    table_html = """
    <style>
        .report-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            table-layout: fixed;
            margin-bottom: 10px;
        }

        .report-table th {
            background-color: #f2f2f2;
            font-weight: 700;
            text-align: center;
            padding: 4px 6px;
            border: 1px solid #d9d9d9;
        }

        .report-table td {
            padding: 4px 6px;
            border: 1px solid #d9d9d9;
            text-align: center;
        }

        .report-table th:first-child,
        .report-table td:first-child {
            text-align: left;
            width: 280px;
            font-weight: 500;
        }

        .report-table tr.total-row td {
            background-color: #d9d9d9;
            font-weight: 700;
        }
    </style>

    <table class="report-table">
        <thead>
            <tr>
    """

    for col in columns:
        table_html += f"<th>{html.escape(str(col))}</th>"

    table_html += """
            </tr>
        </thead>
        <tbody>
    """

    for _, row in section_df.iterrows():
        is_total_row = row.get("Category") == "TOTAL"
        row_class = "total-row" if is_total_row else ""

        table_html += f'<tr class="{row_class}">'

        for col in columns:
            is_category = col == "Category"
            value = format_cell_value(row[col], is_category=is_category)
            table_html += f"<td>{value}</td>"

        table_html += "</tr>"

    table_html += """
        </tbody>
    </table>
    """

    st.markdown(table_html, unsafe_allow_html=True)


def render_dashboard(filtered_df, selected_filters):
    render_report_header(selected_filters)

    sections = build_report_sections(filtered_df)

    for section_name, section_df in sections.items():
        render_section_header(section_name)
        render_static_report_table(section_df)