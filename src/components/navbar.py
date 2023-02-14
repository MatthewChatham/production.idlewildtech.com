import dash_bootstrap_components as dbc
from dash import html

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='assets/logo.png', height="30px", id="logo")),
                        dbc.Col(dbc.NavbarBrand("Idlewild Technologies")),
                    ],
                ),
                href="https://idlewildtech.com/",
                style={"textDecoration": "none"},
            )
        ]
    ),
    color="dark",
    fixed="top",
    dark=True,
)
