# app.py
# This is the main file for the Dash app

# Import the necessary modules
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from libs import helper_funcs as hf

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MORPH])
app.title = 'Py-Nance'

app.layout = html.Div([
    html.H1(children="PyNance", style={'textAlign':'center'}),
    dcc.RangeSlider(id='range-slider',min=1,max=100),
    dcc.Textarea (
        id='data-grid'
        )
])

@callback(
    Output('data-grid','value'),
    Input('range-slider','value')
)
def cold_start(value):
    return str(hf.compound_interest(20000,0.0425,12,(9/12)))
# Run the app on port 8080
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8080, debug=True)
