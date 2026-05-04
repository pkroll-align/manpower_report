import pandas as pd


def find_column(df, possible_names):
    normalized_columns = {
        str(col).lower().strip(): col
        for col in df.columns
    }

    for name in possible_names:
        key = name.lower().strip()
        if key in normalized_columns:
            return normalized_columns[key]

    return None


def get_summary_metrics(df, filtered_df):
    return {
        "total_rows": len(df),
        "filtered_rows": len(filtered_df),
    }


def get_company_summary(filtered_df):
    company_col = find_column(filtered_df, [
        "Company",
        "Contractor",
        "Vendor",
        "B",
        "What company are you logging?",
        "What company are you working for?"
    ])

    if company_col is None:
        return None, None

    summary = (
        filtered_df
        .groupby(company_col, dropna=False)
        .size()
        .reset_index(name="Entries")
        .sort_values("Entries", ascending=False)
    )

    summary[company_col] = summary[company_col].replace("", "Blank")

    return summary, company_col