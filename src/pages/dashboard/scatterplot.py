import plotly.express as px
from dash import dcc
from sqlalchemy import create_engine

from utils import get_df
from utils.settings import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

df = get_df(engine)

y_cols = [c for c in df.columns if c.endswith("Selected Average RBM Position")]
df_melt = df.melt(id_vars=[c for c in df.columns if c not in y_cols])

scatter = dcc.Graph(
    figure=px.scatter(
        data_frame=df_melt, x="Sample Duration (min)", y="value", color="variable"
    )
)
