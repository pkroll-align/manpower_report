def get_summary_metrics(df, filtered_df):
    return {
        "total_rows": len(df),
        "filtered_rows": len(filtered_df),
    }


def get_count_by_column(filtered_df, column_name):
    if column_name not in filtered_df.columns:
        return None

    return (
        filtered_df[column_name]
        .value_counts()
        .reset_index()
        .rename(columns={
            "index": column_name,
            column_name: "Count"
        })
    )