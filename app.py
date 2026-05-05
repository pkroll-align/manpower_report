from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from dash import Dash, Input, Output, dcc, html

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


app = Dash(__name__)
server = app.server


def get_default_adjusted_date():
    now = datetime.now(ZoneInfo(LOCAL_TIMEZONE))

    if now.hour < 9:
        now = now - timedelta(days=1)

    return now.date()


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
            html.Details(
                [
                    html.Summary("Debug"),
                    html.Div(f"Rows used: {len(filtered_df)}"),
                    html.Pre("\n".join(filtered_df.columns)),
                ],
                className="debug-section"
            ),
            *report_sections,
        ]
    )


app.layout = html.Div(
    [
        html.Div(
            [
                html.H2("Filters"),

                html.Label("Date"),
                dcc.DatePickerSingle(
                    id="date-filter",
                    date=get_default_adjusted_date(),
                    display_format="MM/DD/YYYY",
                ),

                html.Label("Shift"),
                dcc.Dropdown(
                    id="shift-filter",
                    options=[
                        {"label": "Day Shift", "value": "Day Shift"},
                        {"label": "Night Shift", "value": "Night Shift"},
                    ],
                    value="Day Shift",
                    clearable=False,
                ),

                html.Label("Time"),
                dcc.Dropdown(
                    id="time-filter",
                    clearable=False,
                ),
            ],
            className="sidebar"
        ),

        html.Div(
            id="report-container",
            className="main-content"
        ),
    ],
    className="app-container"
)


@app.callback(
    Output("time-filter", "options"),
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
    Input("date-filter", "date"),
    Input("shift-filter", "value"),
    Input("time-filter", "value"),
)
def update_report(selected_date, selected_shift, selected_time):
    df = load_sheet_data(SHEET_ID, WORKSHEET_NAME)

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