import streamlit as st


def render_dashboard(df):
    st.subheader("Dashboard")

    st.write("Rows loaded:", len(df))

    with st.expander("View raw data", expanded=False):
        st.dataframe(df, use_container_width=True)

    st.subheader("Available Columns")
    st.write(list(df.columns))