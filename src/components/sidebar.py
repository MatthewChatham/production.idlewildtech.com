import dash_bootstrap_components as dbc
from dash import html
import dash_daq as daq
from dash import dcc, Input, Output, State, ctx, ALL
from utils import get_df, get_dd
import dash

df = get_df()
dd = get_dd()

sidebar_header = dbc.Row(
    [
        dbc.Col(
            [
                html.H2("CNT Production", className="display-7"),
            ]
        ),
        dbc.Col(
            [
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Img(src="assets/filter.svg", className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "border-color": "rgba(0,0,0,.1)",
                    },
                    id="navbar-toggle",
                ),
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    # html.Span(className="navbar-toggler-icon"),
                    html.Img(src="assets/filter.svg", className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "border-color": "rgba(0,0,0,.1)",
                    },
                    id="sidebar-toggle",
                ),
            ],
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width="auto",
            # vertically align the toggle in the center
            align="center",
        ),
    ],
)

filter_modal = html.Div(
    children =
        [
            dbc.Row([
                dbc.Col(
                    dbc.Button(
                        "Adjust filters",
                        id="open",
                        n_clicks=0,
                        style={'margin-right': '5px'}
                    ),
                    className='col-auto'
                ),
                dbc.Col(
                    dbc.Button("Reset", id="reset-filters", n_clicks=0),
                    className='col-auto'
                )
            ],
            className='g-0'
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(
                    [
                        dbc.ModalTitle("Additional Filters")
                    ]
                ),
                html.Div(
                    html.Em('By default, null values are included.'),
                    style={'padding': '1rem'}
                ),
                dbc.ModalBody(html.Div(id='filter-fields')),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="close",
                        className="ms-auto",
                        n_clicks=0
                    )
                ),
            ],
            id="filter-modal",
            size='lg',
            is_open=False,
            fullscreen=False
        ),
    ],
    className='my-2'
)

filters = html.Div([
    dbc.Row([
        dbc.Col(html.H5("Additional Filters"), className='col-auto'),
        dbc.Col(daq.BooleanSwitch(id='filters-switch', on=True), className='col-auto')
    ], className='g-1'),
    html.Div(
        id='filter-field-picker-div',
        children=dcc.Dropdown(
            df.columns,
            [],
            multi=True,
            placeholder='Pick filter fields',
            id='filter-field-picker'
        )
    ),
    filter_modal
])

sidebar = html.Div(
    [
        sidebar_header,
        dbc.Collapse(
            children=[
                filters,
                html.Hr(),
                html.A(
                    "GitHub repository",
                    href="https://github.com/MatthewChatham/production.idlewildtech.com",
                ),
            ],
            id="collapse",
        ),
    ],
    id="sidebar",
    className="collapsed",
)

@dash.callback(
    Output("filter-modal", "is_open"),
    [
        Input("open", "n_clicks"),
        Input("close", "n_clicks")
    ],
    [State("filter-modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


def generate_filter_control(c, df, dd, ctrl_value=None, null_value=None):
    """
    Given a column name `c`,
    generate an appropriate filter control based
    on the column type and values.
    """

    control = None
    res = [
        html.H6(c),
        None
    ]

    print('testing type')
    print(dd)
    print(c in dd)
    print(dd[c])
    try:
        if dd[c] == 'numeric':
            print('got numeric')

            rng = [
                df[c].astype(float).min(),
                df[c].astype(float).max()
            ]

            ctrl_value = ctrl_value if ctrl_value else rng

            control = dcc.RangeSlider(
                *rng,
                value=ctrl_value,
                id={'type': 'filter-control', 'column': c}
            )
        else:
            print('got non-numeric')

            ctrl_value = ctrl_value if ctrl_value else df[c].unique()

            control = dcc.Dropdown(
                df[c].dropna().unique(),
                value=ctrl_value,
                multi=True,
                placeholder=c,
                id={'type': 'filter-control', 'column': c}
            )
    except Exception:
        print('got error')

    null_value = null_value if null_value is not None else ['Include null']

    res[1] = dbc.Row([
        dbc.Col(control, width=8),
        dbc.Col(dcc.Checklist(
            ['Include null'],
            null_value,
            inputStyle={'margin-right': '5px'},
            id={'type': 'filter-null', 'column': c}
        ), width=4)
    ])

    # print('Appending to children:')
    # print(res)

    return html.Div(res, style={'margin-top': '1rem'})

@dash.callback(
    [
        Output('open', 'disabled'),
        Output('reset-filters', 'disabled'),
        Output('filter-field-picker', 'disabled'),
    ],
    Input('filters-switch', 'on')
)
def toggle_filter_controls(apply_filters):
    if apply_filters:
        return [False]*3
    else:
        return [True]*3

@dash.callback(
    [
        Output('filter-fields', 'children'),
        Output('filter-field-picker', 'value')
    ],
    [
        Input('filter-field-picker', 'value'),
        Input('reset-filters', 'n_clicks')
    ],
    [
        State({'type': 'filter-control', 'column': ALL}, 'value'),
        State({'type': 'filter-control', 'column': ALL}, 'id'),
        State({'type': 'filter-null', 'column': ALL}, 'value')
    ]
)
def display_filter_controls(
        value,
        n_clicks,
        ctrl_values,
        ctrl_idx,
        null_values
):
    if ctx.triggered_id == 'reset-filters':
        return [], []

    df = get_df()
    dd = get_dd()

    res = [[], value]

    existing_cols = set([i['column'] for i in ctrl_idx])

    for i, c in enumerate(value):
        if c in existing_cols:
            res[0].append(
                generate_filter_control(
                    c,
                    df, dd,
                    ctrl_values[i],
                    null_values[i]
                )
            )
        else:
            print(c)
            res[0].append(generate_filter_control(c, df, dd))

    return res