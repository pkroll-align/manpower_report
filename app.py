from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from dash import Dash, Input, Output, html
import dash_mantine_components as dmc

from utils.sheets import load_sheet_data
from utils.data_filters import (
    DAY_SHIFT_TIMES,
    NIGHT_SHIFT_TIMES,
    apply_report_filters,
)
from utils.calculations import build_report_sections


SHEET_ID = "1ZRTbCI0b7q1OjEf5NOn-IZbVgmetqGkF0Koa4xxliI4"
WORKSHEET_NAME = "Day Form Responses"
LOCAL_TIMEZONE = "America/Chicago"

# Auto-refresh interval in milliseconds.
# 60,000 = refresh once per minute.
AUTO_REFRESH_INTERVAL_MS = 60000


app = Dash(__name__)
server = app.server


def get_default_adjusted_date():
    now = datetime.now(ZoneInfo(LOCAL_TIMEZONE))

    if now.hour < 9:
        now = now - timedelta(days=1)

    return now.date().isoformat()


def build_report_table(section_df):
    header = html.Tr([
        html.Th(col) for col in section_df.columns
    ])

    body_rows = []

    for _, row in section_df.iterrows():
        is_total = row["Category"] == "TOTAL"

        cells = []

        for col in section_df.columns:
            if col == "Category":
                cells.append(html.Td(row[col]))
            else:
                try:
                    cells.append(html.Td(f"{float(row[col]):,.0f}"))
                except (ValueError, TypeError):
                    cells.append(html.Td(""))

        body_rows.append(
            html.Tr(
                cells,
                className="total-row" if is_total else ""
            )
        )

    return html.Table(
        [html.Thead(header), html.Tbody(body_rows)],
        className="report-table"
    )


def build_debug_table(filtered_df):
    debug_cols = [
        "Timestamp",
        "Adjusted Date",
        "Company:",
        "Which shift?",
        "Time",
    ]

    available_debug_cols = [
        col for col in debug_cols
        if col in filtered_df.columns
    ]

    if filtered_df.empty:
        return html.Div("No rows are being used for this report.")

    if not available_debug_cols:
        return html.Div("No debug columns were found in the filtered data.")

    header = html.Tr([
        html.Th(col) for col in available_debug_cols
    ])

    body_rows = []

    for _, row in filtered_df[available_debug_cols].iterrows():
        body_rows.append(
            html.Tr([
                html.Td(str(row[col])) for col in available_debug_cols
            ])
        )

    return html.Table(
        [html.Thead(header), html.Tbody(body_rows)],
        className="debug-table"
    )


def build_report_layout(filtered_df, selected_date, selected_shift, selected_time):
    sections = build_report_sections(filtered_df)

    report_sections = []

    for section_name, section_df in sections.items():
        report_sections.append(
            html.Div(
                [
                    html.Div(section_name, className="section-header"),
                    build_report_table(section_df),
                ],
                className="report-section"
            )
        )

    return html.Div(
        [
            html.H3("Manpower Report"),
            html.Div(
                [
                    html.Div([html.Strong("Date: "), str(selected_date)], className="report-pill"),
                    html.Div([html.Strong("Shift: "), selected_shift], className="report-pill"),
                    html.Div([html.Strong("Time: "), selected_time], className="report-pill"),
                ],
                className="report-header"
            ),
            *report_sections,
            html.Details(
                [
                    html.Summary("Debug - rows used in report"),
                    html.Div(f"Rows used: {len(filtered_df)}"),
                    html.Div(
                        f"Last refreshed: {datetime.now(ZoneInfo(LOCAL_TIMEZONE)).strftime('%m/%d/%Y %I:%M:%S %p')}"
                    ),
                    build_debug_table(filtered_df),
                ],
                className="debug-section"
            ),
        ]
    )


app.layout = dmc.MantineProvider(
    html.Div(
        [
            html.Div(
                [
                    html.H2("Filters"),

                    html.Label("Date"),
                    html.Div(
                        dmc.DatePicker(
                            id="date-filter",
                            value=get_default_adjusted_date(),
                            allowDeselect=False,
                        ),
                        className="calendar-wrapper",
                    ),

                    html.Label("Shift"),
                    dmc.Select(
                        id="shift-filter",
                        data=[
                            {"label": "Day Shift", "value": "Day Shift"},
                            {"label": "Night Shift", "value": "Night Shift"},
                        ],
                        value="Day Shift",
                        allowDeselect=False,
                        searchable=False,
                        size="sm",
                        className="filter-select",
                    ),

                    html.Label("Time"),
                    dmc.Select(
                        id="time-filter",
                        data=[],
                        value=None,
                        allowDeselect=False,
                        searchable=False,
                        size="sm",
                        className="filter-select",
                    ),
                ],
                className="sidebar"
            ),

            html.Div(
                id="report-container",
                className="main-content"
            ),

            html.Div(
                id="auto-refresh-container",
                children=[
                    # This triggers the report callback every minute.
                    dmc.Text("", style={"display": "none"}),
                ],
                style={"display": "none"},
            ),

            # Dash interval component for live updates
            __import__("dash").dcc.Interval(
                id="auto-refresh-interval",
                interval=AUTO_REFRESH_INTERVAL_MS,
                n_intervals=0,
            ),
        ],
        className="app-container"
    )
)


@app.callback(
    Output("time-filter", "data"),
    Output("time-filter", "value"),
    Input("shift-filter", "value"),
)
def update_time_options(selected_shift):
    if selected_shift == "Night Shift":
        times = NIGHT_SHIFT_TIMES
    else:
        times = DAY_SHIFT_TIMES

    options = [{"label": t, "value": t} for t in times]

    return options, times[0]


@app.callback(
    Output("report-container", "children"),
    Input("date-filter", "value"),
    Input("shift-filter", "value"),
    Input("time-filter", "value"),
    Input("auto-refresh-interval", "n_intervals"),
)
def update_report(selected_date, selected_shift, selected_time, n_intervals):
    df = load_sheet_data(
        SHEET_ID,
        WORKSHEET_NAME,
        force_refresh=True,
    )

    filtered_df = apply_report_filters(
        df,
        selected_date,
        selected_shift,
        selected_time
    )

    return build_report_layout(
        filtered_df,
        selected_date,
        selected_shift,
        selected_time
    )


if __name__ == "__main__":
    app.run(debug=True)