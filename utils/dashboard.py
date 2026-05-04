import streamlit as st


def render_dashboard(filtered_df):
    st.subheader("Filtered Data")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    st.write("Rows loaded:", len(filtered_df))

    with st.expander("Column names"):
        st.write(list(filtered_df.columns))