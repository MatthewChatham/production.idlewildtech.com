import numpy as np
import plotly.express as px
from dash import dcc, html, dash_table, Input, Output, ALL
import dash
import pandas as pd
from utils import get_df, get_dd, get_filter_mask, predict_polynomial, colnames, plotnames, argnames

actual_by_predicted = html.Div([
    html.B("Actual Versus Predicted"),
    html.Div(id='actual-by-predicted-div'),
    html.Div(id='actual-by-predicted-table-div')
], id='actual-vs-predicted-div')

@dash.callback(
    Output('actual-by-predicted-div', 'children'),
    Input('filters-switch', 'on'),
    Input({'type': 'filter-control', 'column': ALL}, 'value'),
    Input({'type': 'filter-control', 'column': ALL}, 'id'),
    Input({'type': 'filter-null', 'column': ALL}, 'value')
)
def update_scatter(
    apply_filters,
    ctrl_values,
    ctrl_idx,
    null_values
):
    df = get_df()
    dd = get_dd()

    filter_mask = get_filter_mask(
        df, dd,
        ctrl_values,
        ctrl_idx,
        null_values,
        apply_filters
    )

    df = df[filter_mask]

    df_melt = df.melt(id_vars=[c for c in df.columns if 'Selected Average RBM Position' not in c])
    df_melt['Wavelength (nm)'] = df_melt['variable'].map(lambda s: s[:3]).astype(int)

    kwargs = {k:df_melt[colnames[i]] for i,k in enumerate(argnames)}
    preds = predict_polynomial(**kwargs)
    y = df_melt['value']

    fig = px.scatter(x=preds, y=y, color_discrete_sequence=['black'])
    x_red = np.linspace(140, 270)
    y_red = 0 + 1 * x_red
    fig.add_scatter(x=x_red, y=y_red)
    fig.add_hline(y=y.mean(), line_color="blue")

    return dcc.Graph(figure=fig)

@dash.callback(
    Output('actual-by-predicted-table-div', 'children'),
    Input('filters-switch', 'on'),
    Input({'type': 'filter-control', 'column': ALL}, 'value'),
    Input({'type': 'filter-control', 'column': ALL}, 'id'),
    Input({'type': 'filter-null', 'column': ALL}, 'value')
)
def update_abp_table(
    apply_filters,
    ctrl_values,
    ctrl_idx,
    null_values
):
    df = get_df()
    dd = get_dd()

    filter_mask = get_filter_mask(
        df, dd,
        ctrl_values,
        ctrl_idx,
        null_values,
        apply_filters
    )

    df = df[filter_mask]

    df_melt = df.melt(id_vars=[c for c in df.columns if 'Selected Average RBM Position' not in c])
    df_melt['Wavelength (nm)'] = df_melt['variable'].map(lambda s: s[:3]).astype(int)

    kwargs = {k:df_melt[colnames[i]] for i,k in enumerate(argnames)}
    preds = predict_polynomial(**kwargs)
    y = df_melt['value']

    fig = px.scatter(x=preds, y=y, color_discrete_sequence=['black'])
    x_red = np.linspace(140, 270)
    y_red = 0 + 1 * x_red
    fig.add_scatter(x=x_red, y=y_red)
    fig.add_hline(y=y.mean(), line_color="blue")

    table_title = html.Em('Model Metrics')
    table_df = pd.DataFrame({'Metric': ['RMSE', 'RSq', 'P-Value'], 'Value': [19.937, 0.63, '<.0001']})
    table = html.Div(id='avp-table-div', children=[
        table_title,
        dash_table.DataTable(
            data=table_df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in table_df.columns]
        )
    ])

    return table