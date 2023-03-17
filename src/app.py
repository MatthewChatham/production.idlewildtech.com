import dash_bootstrap_components as dbc
from dash import Dash, page_container

from components import navbar, footer

meta = {'name': "viewport", 'content': "width=device-width, initial-scale=1"}

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[meta],
)

app.layout = dbc.Container(
    [navbar, page_container, footer], id="page-container", fluid=True
)

server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
