import numpy as np
import plotly.express as px
from dash import dcc, html, dash_table
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash
from dash import html, Input, Output, State
from utils import get_df, predict_polynomial, colnames, plotnames, argnames

fig = make_subplots(rows=1, cols=2)

df = get_df()

# Melt the dataframe
df_melt = df.melt(id_vars=[c for c in df.columns if 'Selected Average RBM Position' not in c])
df_melt['Wavelength (nm)'] = df_melt['variable'].map(lambda s: s[:3]).astype(int)
df_melt = df_melt[df_melt['value'].notnull() & (df_melt['Water (%) fuel '] < 48)]

means = [df_melt[v].mean() for v in colnames]
ranges = [(df_melt[v].min(), df_melt[v].max()) for v in colnames]
ranges = [(int(t[0]), int(t[1])) if argnames[i] != 'co2' else t for i,t in enumerate(ranges)]

# 'Standardized data or preliminary data[Preliminary]': df_melt['Standardized data or preliminary data'] == 'Preliminary',
# 'Standardized data or preliminary data[Standard]': df_melt['Standardized data or preliminary data'] == 'Standard'

sliders = [dcc.Slider(*ranges[i], value=means[i], id=v, tooltip={"placement": "bottom", "always_visible": True}) for i,v in enumerate(argnames)]
sliders = [html.Span([colnames[i], sliders[i]]) for i,v in enumerate(argnames)]
sliders += [dbc.Button('Reset', id='slider-reset')]

profiler = dbc.Row([
    dbc.Col(sliders, md=6, sm=12),
    dbc.Col(dcc.Graph(id='subplots'), md=6, sm=12)
])

profiler = html.Div([
    html.B("Prediction Profiler"),
    profiler
], id='profiler')

@dash.callback(
    Output('subplots', 'figure'),
    [Input(v, 'value') for v in argnames]
)
def update_profiler(*sliders):
    def get_profile(arg):
        x = np.linspace(*ranges[argnames.index(arg)])
        args = dict(zip(argnames, sliders))
        args[arg] = x
        y = predict_polynomial(**args)
        return x, y

    profiles = [get_profile(a) for a in argnames]
    graphs = [list(px.scatter(x=p[0], y=p[1]).select_traces())[0] for p in profiles]

    subplots = make_subplots(rows=2, cols=4, subplot_titles=plotnames, shared_yaxes=True)
    for i, g in enumerate(graphs):
        row = 1 if i <= 3 else 2
        col = (i % 4) + 1
        subplots.add_trace(g, row=row, col=col)

    subplots.update_yaxes(range=[130, 270])
    subplots.update_annotations(font_size=12)

    return subplots

@dash.callback(
    [Output(v, 'value') for v in argnames],
    Input('slider-reset', 'n_clicks')
)
def reset_sliders(n_clicks):
    return means