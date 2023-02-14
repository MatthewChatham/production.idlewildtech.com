import dash
from dash import html, Input, Output, State
import dash_bootstrap_components as dbc

from components.sidebar import sidebar

dash.register_page(__name__, path="/", title='CNT Production')

content = html.Div(id="page-content", children=["Under construction"])


def serve_layout():
    return dbc.Container(
        [sidebar, content],
        id="container",
        fluid=True,
    )


@dash.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    if n and classname == "collapsed":
        return ""
    return "collapsed"


layout = serve_layout
