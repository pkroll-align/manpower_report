import pandas as pd

COMPANY_COL = "Company:"
TOTAL_PERSONNEL_COL = "Total number of personnel (including Leads/Supervisors)"

COMPANIES = [
    "Agility",
    "AIS",
    "Circet",
    "Flex",
    "Infinite Cloud",
    "SSS",
    "TDS",
]

REPORT_SECTIONS = {
    "Total Manpower": {
        "Total Reported Count": TOTAL_PERSONNEL_COL,
    },
    "Warehouse": {
        "Leads/Supervisors": "Warehouse Leads/Supervisors",
        "Labeling": "Labeling",
        "QC/Relabeling": "QC/Relabeling",
        "Pre-Staging": "Pre-Staging Cable after QC",
        "Staging": "Staging Cable on DH floor for pulls",
    },
}


def to_number(series):
    return pd.to_numeric(series, errors="coerce").fillna(0)


def build_section(df, section_rows):
    report_rows = []

    for label, source_col in section_rows.items():
        row = {"Category": label}

        for company in COMPANIES:
            company_df = df[df[COMPANY_COL] == company]

            if source_col in df.columns:
                row[company] = int(to_number(company_df[source_col]).sum())
            else:
                row[company] = 0

        row["Total"] = sum(row[company] for company in COMPANIES)

        report_rows.append(row)

    section_df = pd.DataFrame(report_rows)

    total_row = {"Category": "TOTAL"}

    for col in ["Total", *COMPANIES]:
        total_row[col] = int(section_df[col].sum())

    section_df = pd.concat(
        [section_df, pd.DataFrame([total_row])],
        ignore_index=True
    )

    return section_df[["Category", "Total", *COMPANIES]]


def build_report_sections(df):
    sections = {}

    for section_name, section_rows in REPORT_SECTIONS.items():
        sections[section_name] = build_section(df, section_rows)

    return sections