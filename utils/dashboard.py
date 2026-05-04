import streamlit as st

from utils.calculations import get_summary_metrics


def render_dashboard(df, filtered_df):
    metrics = get_summary_metrics(df, filtered_df)

    st.subheader("Dashboard Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Rows", metrics["total_rows"])

    with col2:
        st.metric("Filtered Rows", metrics["filtered_rows"])

    st.subheader("Filtered Data")
    st.dataframe(filtered_df, use_container_width=True)

    with st.expander("Column names"):
        st.write(list(df.columns))