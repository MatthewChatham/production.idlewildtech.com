import numpy as np
import plotly.express as px
from dash import dcc, html, dash_table
import pandas as pd

intercept = 227.45178

# simplified case with two variables
coef = np.array(
    [-0.015264, 0.2842928, -0.079529, 10.739164, 148.41761, -20.53263, -2.044141, 0.0148309, 0.000233, -0.062851,
        -276.9074, -47.48542, -115.822, 0.0036535, 0.019878, 0.0052762, 0.1330904, 0.0201388, -6.954154, -1.369383, ])

df = pd.read_csv('../src/assets/df_clean.csv')

# Melt the dataframe
df_melt = df.melt(id_vars=[c for c in df.columns if 'Selected Average RBM Position' not in c])
df_melt['Wavelength (nm)'] = df_melt['variable'].map(lambda s: s[:3]).astype(int)

df_melt = df_melt[df_melt['value'].notnull() & (df_melt['Water (%) fuel '] < 48)]

cols = ['Wavelength (nm)', 'Local DewPoint (F) ', 'Reactor Temp (C)', 'Ar (SLPM)', 'CO2 (SLPM)', 'H2 (SLPM)',
    'Water (%) fuel ', ]

X = df_melt[cols].values

V1 = ['Local DewPoint (F) ', 'Reactor Temp (C)', 'Wavelength (nm)', 'CO2 (SLPM)', 'Ar (SLPM)', 'CO2 (SLPM)',
    'Wavelength (nm)', 'Local DewPoint (F) ', 'Reactor Temp (C)', 'Water (%) fuel ', ]

V2 = ['Local DewPoint (F) ', 'Reactor Temp (C)', 'Ar (SLPM)', 'CO2 (SLPM)', 'H2 (SLPM)', 'H2 (SLPM)', 'Water (%) fuel ',
    'Water (%) fuel ', 'Water (%) fuel ', 'Water (%) fuel ', ]

T1 = [42.3221, 859.854, 692.14, 0.10321, 0.45553, 0.10321, 692.14, 42.3221, 859.854, 5.36035, ]

T2 = [42.3221, 859.854, 0.45553, 0.10321, 0.13925, 0.13925, 5.36035, 5.36035, 5.36035, 5.36035, ]


def add_var(v1, v2, t1, t2):
    newvar = (df_melt[v1] - t1) * (df_melt[v2] - t2)
    newvar = newvar.values.reshape(-1, 1)
    return np.append(X, newvar.reshape(-1, 1), axis=1)


for vals in zip(V1, V2, T1, T2):
    X = add_var(*vals)

newvar = df_melt['Time since initital precusor Turn-on (min)'].values.reshape(-1, 1)
X = np.append(X, newvar.reshape(-1, 1), axis=1)

newvar = (df_melt['Standardized data or preliminary data'] == 'Preliminary').values.reshape(-1, 1)
X = np.append(X, newvar.reshape(-1, 1), axis=1)

newvar = (df_melt['Standardized data or preliminary data'] == 'Standard').values.reshape(-1, 1)
X = np.append(X, newvar.reshape(-1, 1), axis=1)

y = df_melt['value'].values
preds = intercept + (coef * X).sum(axis=1)

fig = px.scatter(x=preds, y=y, color_discrete_sequence=['black'])
x_red = np.linspace(140, 270)
y_red = 0 + 1 * x_red
fig.add_scatter(x=x_red, y=y_red)
fig.add_hline(y=y.mean(), line_color="blue")

graph = dcc.Graph(figure=fig)

table_title = html.Em('Model Metrics')
table_df = pd.DataFrame({'Metric': ['RMSE', 'RSq', 'P-Value'], 'Value': [19.937, 0.63, '<.0001']})
table = html.Div(id='avp-table-div', children=[
    table_title,
    dash_table.DataTable(
        data=table_df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in table_df.columns]
    )
])

actual_by_predicted = html.Div([

    html.B("Actual Versus Predicted"),
    graph,
    table
], id='actual-vs-predicted-div')
