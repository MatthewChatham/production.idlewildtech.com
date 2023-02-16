import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html, Input, Output, State
import dash
from utils import get_df

dropdown_options = ['Sample Duration (min)', 'Number of Run Days on Tube', 'Lab Humidity (%)', 'Lab Temp (C)',
                    'Local DewPoint (F) ', 'Reactor Temp (C)', 'ferrocene (g)', 'water (g)', 'fuel (mL/h)', 'Ar (SLPM)',
                    'CO2 (SLPM)', 'H2 (SLPM)']
df = get_df()
dropdown_options += [c for c in df.columns if c not in dropdown_options]

scatter = html.Div([

    html.B("Average RBM Position vs Selected Variable"), dbc.Row([

        dbc.Col(dcc.Dropdown(dropdown_options, 'Sample Duration (min)', multi=False, clearable=False, placeholder='Pick X-axis',
                             id='scatter-xaxis-dropdown'), md=3, sm=6), dbc.Col(
            dcc.Checklist(['Log Y', 'Squash'], ['Log Y'], id='scatter-opts', inline=True,
                          inputStyle={'margin-right': '5px'}, labelStyle={'margin-right': '10px'}), md=6, sm=7,
            className='pt-2')], className='mb-2'),

    dbc.Row([dbc.Col(id='scatter')])
]
)

@dash.callback(
    Output('scatter', 'children'),
    Input('scatter-xaxis-dropdown', 'value'),
    Input('scatter-opts', 'value')
)
def update_scatter(x, opts):
    df = get_df()

    y_cols = [c for c in df.columns if c.endswith("Selected Average RBM Position")]
    df_melt = df.melt(id_vars=[c for c in df.columns if c not in y_cols])

    return dcc.Graph(
        figure=px.scatter(
            data_frame=df_melt,
            x=x,
            y="value",
            color="variable" if 'Squash' not in opts else None,
            log_y='Log Y' in opts
        )
    )
