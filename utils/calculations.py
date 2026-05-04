import pandas as pd

COMPANY_COL = "Company:"

COMPANIES = [
    "Agility",
    "AIS",
    "Circet",
    "Flex",
    "Infinite Cloud",
    "SSS",
    "TDS",
]

TOTAL_PERSONNEL_COL = "Total number of personnel (including Leads/Supervisors)"


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

    "DH15": {
        "Leads/Supervisors": "DH15 Leads/Supervisors",
        "T1 Sidecart Dressing SMF (AS-T1/R.T1-T2)": "DH15 T1 Sidecart Dressing SMF (AS-T1/R.T1-T2)",
        "Patching T1 SMF (AS-T1/R.T1-T2)": "DH15 Patching T1 SMF (AS-T1/R.T1-T2)",
        "Patching GPU-T1 CAT6": "DH15 Patching GPU-T1 CAT6",
        "Patching AEC": "DH15 Patching AEC",
        "Patching IPMI": "DH15 Patching IPMI",
        "Network Row Sidecart Dressing SMF": "DH15 Network Row Sidecart Dressing SMF",
        "Network Row Patching SMF": "DH15 Network Row Patching SMF",
        "Patching (NA/NB) Mgmt CAT6": "DH15 Patching (NA/NB) Mgmt CAT6",
        "QC/Monitoring": "DH15 QC/Monitoring",
        "Copper Testing": "DH15 Copper Testing",
        "Fiber Testing": "DH15 Fiber Testing",
    },

    "DH13": {
        "Leads/Supervisors": "DH13 Leads/Supervisors",
        "T1 Sidecart Dressing SMF (AS-T1/R.T1-T2)": "DH13 T1 Sidecart Dressing SMF (AS-T1/R.T1-T2)",
        "Patching T1 SMF (AS-T1/R.T1-T2)": "DH13 Patching T1 SMF (AS-T1/R.T1-T2)",
        "Patching GPU-T1 CAT6": "DH13 Patching GPU-T1 CAT6",
        "Patching AEC": "DH13 Patching AEC",
        "Patching IPMI": "DH13 Patching IPMI",
        "Network Row Sidecart Dressing SMF": "DH13 Network Row Sidecart dressing SMF",
        "Network Row Patching SMF": "DH13 Network Row Patching SMF",
        "Patching (NA/NB) Mgmt CAT6": "DH13 Patching (NA/NB) Mgmt CAT6",
        "QC/Monitoring": "DH13 QC/Monitoring",
        "Copper Testing": "DH13 Copper Testing",
        "Fiber Testing": "DH13 Fiber Testing",
    },

    "DH18": {
        "Leads/Supervisors": "DH18 Leads/Supervisors",
        "T1 Sidecart Dressing SMF (AS-T1/R.T1-T2)": "DH18 T1 Sidecart Dressing SMF (AS-T1/R.T1-T2)",
        "Patching T1 SMF (AS-T1/R.T1-T2)": "DH18 Patching T1 SMF (AS-T1/R.T1-T2)",
        "Patching GPU-T1 CAT6": "DH18 Patching GPU-T1 CAT6",
        "Patching AEC": "DH18 Patching AEC",
        "Patching IPMI": "DH18 Patching IPMI",
        "Network Row Sidecart Dressing SMF": "DH18 Network Row Sidecart dressing SMF",
        "Network Row Patching SMF": "DH18 Network Row Patching SMF",
        "Patching (NA/NB) Mgmt CAT6": "DH18 Patching (NA/NB) Mgmt CAT6",
        "QC/Monitoring": "DH18 QC/Monitoring",
        "Copper Testing": "DH18 Copper Testing",
        "Fiber Testing": "DH18 Fiber Testing",
    },

    "DH20": {
        "Leads/Supervisors": "DH20 Leads/Supervisors",
        "T1 Sidecart Dressing SMF (AS-T1/R.T1-T2)": "DH20 T1 Sidecart Dressing SMF (AS-T1/R.T1-T2)",
        "Patching T1 SMF (AS-T1/R.T1-T2)": "DH20 Patching T1 SMF (AS-T1/R.T1-T2)",
        "Patching GPU-T1 CAT6": "DH20 Patching GPU-T1 CAT6",
        "Patching AEC": "DH20 Patching AEC",
        "Patching IPMI": "DH20 Patching IPMI",
        "Network Row Sidecart Dressing SMF": "DH20 Network Row Sidecart dressing SMF",
        "Network Row Patching SMF": "DH20 Network Row Patching SMF",
        "Patching (NA/NB) Mgmt CAT6": "DH20 Patching (NA/NB) Mgmt CAT6",
        "QC/Monitoring": "DH20 QC/Monitoring",
        "Copper Testing": "DH20 Copper Testing",
        "Fiber Testing": "DH20 Fiber Testing",
    },

    "Supercore": {
        "Leads/Supervisors": "SC Leads/Supervisors",
        "SMF Dressing": "SC SMF Dressing",
        "SMF Patching": "SC SMF Patching",
        "SMF QC/Monitoring": "SC SMF QC/Monitoring",
        "SMF Testing": "SC SMF Testing",
    },
}


def to_number(series):
    return pd.to_numeric(series, errors="coerce").fillna(0)


def sum_by_company(df, source_col):
    row = {}

    for company in COMPANIES:
        company_rows = df[df[COMPANY_COL] == company]

        if source_col in df.columns:
            row[company] = int(to_number(company_rows[source_col]).sum())
        else:
            row[company] = 0

    row["Total"] = sum(row[company] for company in COMPANIES)

    return row


def build_report_section(df, rows_map):
    report_rows = []

    for label, source_col in rows_map.items():
        row = sum_by_company(df, source_col)
        row["Category"] = label
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

    for section_name, rows_map in REPORT_SECTIONS.items():
        sections[section_name] = build_report_section(df, rows_map)

    return sections