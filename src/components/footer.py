from dash import html, dcc

CITATION = """
Bulmer, J. S., Kaniyoor, A., Elliott 2008432, J. A., A Meta-Analysis
of Conductive and Strong Carbon Nanotube Materials. Adv. Mater. 2021, 33,
2008432.
"""
CITELINK = "https://doi.org/10.1002/adma.202008432"

citation = html.Em(
    [CITATION, html.A(CITELINK, href=CITELINK)], className="text-muted", id="citation"
)

clipboard = dcc.Clipboard(
    target_id="citation",
    title="copy",
    style={
        "display": "inline-block",
        "fontSize": 15,
        "verticalAlign": "top",
        "margin-right": "5px",
    },
)

footer = html.Footer(id="footer", children=[clipboard, citation])
