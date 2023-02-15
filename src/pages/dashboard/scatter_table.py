from dash import dash_table, html, Output, Input
import dash
from utils import get_df
import scipy.stats as stats
import pandas as pd

scatter_table = html.Div(id='scatter-table')

@dash.callback(
    Output('scatter-table', 'children'),
    Input('scatter-xaxis-dropdown', 'value'),
    Input('scatter-opts', 'value')
)
def update_scatter_table(x, opts):

    df = get_df()

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
            table_df.loc[y, 'Correlation'] = r
            table_df.loc[y, 'P-Value'] = p

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