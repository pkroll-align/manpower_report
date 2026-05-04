import streamlit as st

from utils.calculations import get_summary_metrics, get_company_summary


def render_dashboard(df, filtered_df):
    metrics = get_summary_metrics(df, filtered_df)
    company_summary, company_col = get_company_summary(filtered_df)

    st.subheader("Dashboard Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Rows", metrics["total_rows"])

    with col2:
        st.metric("Filtered Rows", metrics["filtered_rows"])

    st.subheader("Company Breakdown")

    if company_summary is None:
        st.warning("Could not find a company column.")
        with st.expander("Available columns"):
            st.write(list(df.columns))
    else:
        st.caption(f"Grouped by: `{company_col}`")
        st.dataframe(company_summary, use_container_width=True, hide_index=True)

        st.bar_chart(
            company_summary,
            x=company_col,
            y="Entries"
        )

    with st.expander("Filtered raw data"):
        st.dataframe(filtered_df, use_container_width=True)

    with st.expander("Column names"):
        st.write(list(df.columns))