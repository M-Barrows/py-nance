import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/',
    title='PyNance',
    name='PyNance'
    )

layout =  dbc.Container([
    html.H1(["PyNance"]),
    html.H2(["Finance tools built in Python"])
])