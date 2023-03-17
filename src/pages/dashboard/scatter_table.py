from dash import dash_table, html, Output, Input, ALL
import dash
from utils import get_df, get_dd, get_filter_mask
import scipy.stats as stats
import pandas as pd

table_title = html.Em('Correlation Tables Selected Variable vs Average RBM Position')

scatter_table = html.Div(id='scatter-table-div', children=[
    table_title,
    html.Div(id='scatter-table')
])

@dash.callback(
    Output('scatter-table', 'children'),
    Input('scatter-xaxis-dropdown', 'value'),
    Input('scatter-opts', 'value'),
    Input('filters-switch', 'on'),
    Input({'type': 'filter-control', 'column': ALL}, 'value'),
    Input({'type': 'filter-control', 'column': ALL}, 'id'),
    Input({'type': 'filter-null', 'column': ALL}, 'value')
)
def update_scatter_table(
    x,
    opts,
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

    y_cols = [c for c in df.columns if c.endswith("Selected Average RBM Position")]
    df_melt = df.melt(id_vars=[c for c in df.columns if c not in y_cols])

    if not 'Squash' in opts:

        table_df = pd.DataFrame(index=y_cols, columns=['Correlation', 'P-Value'])

        for y in y_cols:
            mask = df_melt['value'].notnull() & df_melt[x].notnull()

            r,p = stats.pearsonr(
                df_melt.loc[(df_melt['variable'] == y) & mask, x],
                df_melt.loc[(df_melt['variable'] == y) & mask, 'value'],
            )
            table_df.loc[y, 'Correlation'] = round(r, 2)
            table_df.loc[y, 'P-Value'] = round(p, 2)

        table_df = table_df.reset_index().rename({'index': 'Output Var'}, axis=1)

        return dash_table.DataTable(
            data=table_df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in table_df.columns]
        )

    else:

        table_df = pd.DataFrame(index=['All'], columns=['Correlation', 'P-Value'])

        mask = df_melt['value'].notnull() & df_melt[x].notnull()

        r, p = stats.pearsonr(
            df_melt.loc[mask, x],
            df_melt.loc[mask, 'value'],
        )
        table_df['Correlation'] = r
        table_df['P-Value'] = p

        table_df = table_df.reset_index().rename({'index': 'Output Var'}, axis=1)

        return dash_table.DataTable(
            data=table_df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in table_df.columns]
        )