import dash_bootstrap_components as dbc
from dash import html

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

sidebar = html.Div(
    [
        sidebar_header,
        dbc.Collapse(
            children=[
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
