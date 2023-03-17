import dash
import dash_bootstrap_components as dbc
from components.sidebar import sidebar
from dash import html, Input, Output, State

from .scatterplot import scatter
from .scatter_table import  scatter_table
from .actual_by_predicted_plot import actual_by_predicted
from .prediction_profiler import profiler

dash.register_page(__name__, path="/", title='CNT Production')

content = html.Div(id="page-content", children=[scatter, scatter_table, actual_by_predicted, profiler])

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
