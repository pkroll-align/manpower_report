import streamlit as st


def render_dashboard(df, filtered_df):
    st.subheader("Dashboard Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Rows", len(df))

    with col2:
        st.metric("Filtered Rows", len(filtered_df))

    st.subheader("Filtered Data")
    st.dataframe(filtered_df, use_container_width=True)

    with st.expander("Column names"):
        st.write(list(df.columns))