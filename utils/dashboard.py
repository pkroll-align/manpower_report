import streamlit as st

from utils.calculations import build_report_sections


def render_report_table(section_df):
    styled_df = section_df.style.apply(
        lambda row: [
            "font-weight: bold; background-color: #d9d9d9;"
            if row["Category"] == "TOTAL"
            else ""
            for _ in row
        ],
        axis=1
    )

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )


def render_dashboard(filtered_df):
    st.subheader("Report Summary")

    sections = build_report_sections(filtered_df)

    for section_name, section_df in sections.items():
        st.markdown(f"### {section_name}")
        render_report_table(section_df)

    with st.expander("Filtered raw data"):
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    with st.expander("Column names"):
        st.write(list(filtered_df.columns))