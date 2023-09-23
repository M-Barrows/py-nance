# app.py
# This is the main file for the Dash app

# Import the necessary modules
import dash
from dash import dcc, html, callback, dash_table
from dash.dash_table import DataTable, FormatTemplate
from dash.dependencies import Input, Output, State
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash_bootstrap_templates import ThemeSwitchAIO
from libs import helper_funcs as hf
from components.navbar import navbar
from theme.config import (LIGHT_THEME_TEMPLATE, LIGHT_THEME_URL, DARK_THEME_TEMPLATE, DARK_THEME_URL)

load_figure_template(['minty','solar'])

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css"
)


app = dash.Dash(__name__, external_stylesheets=[LIGHT_THEME_URL,dbc_css], use_pages=True,url_base_pathname="/apps/pynance/")
app.title = 'Py-Nance'

app.layout = dbc.Container([
    navbar,
    dash.page_container
],className='dbc dbc-ag-grid',fluid=True)


# Run the app on port 8080
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8080, debug=True)
