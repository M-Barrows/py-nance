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