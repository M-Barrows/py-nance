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

money = FormatTemplate.money(2)
app = dash.Dash(__name__, external_stylesheets=[LIGHT_THEME_URL,dbc_css])
app.title = 'Py-Nance'


cd_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([dbc.Label("Principal"), dbc.Input(value = 20_000,id='principal', type='number')],sm=6),
                dbc.Col([dbc.Label("Interest Rate"), dbc.Input(value = 4.25,id='rate', type='number')],sm=6),
            ]),
            dbc.Row([
                dbc.Col([dbc.Label("Compound Periods per Year"), dbc.Input(value = 12,id='compound_n', type='number')],sm=6),
                dbc.Col([dbc.Label("CD Length (years)"), dbc.Input(value = 0.75,id='compound_t', type='number')],sm=6),
            ]),
            dbc.Row([
                dbc.Col([dbc.Label("Times Reinvested"), dbc.Input(value = 30,id='n_terms', type='number')],sm=6),
                dbc.Col([dbc.Label("Reinvestment %"), dbc.Input(value = 100,id='reinvest_percent', type='number')],sm=6),
            ]),
            dbc.Row([dbc.Card([dbc.CardHeader([html.H5(["Total Interest Earned"])]),dbc.CardBody([html.H1([],id='total-interest-callout')])])],class_name='my-5 mx-2')
        ],lg=4, align='start'),
        dbc.Col([
            dcc.Graph(
                id='data-chart',

            )
        ],lg=8, align='center', class_name='mx-2 mb-3')
    ]),
    dbc.Row([
        dash_table.DataTable(
            columns=[
                {"name":"Term","id":"Term"},
                {"name":"Term_Principal","id":"Term_Principal", "type": 'numeric',"format": money},
                {"name":"Term_Interest","id":"Term_Interest", "type": 'numeric',"format": money},
                {"name":"Total_Interest","id":"Total_Interest", "type": 'numeric',"format": money},
                {"name":"Total_Value","id":"Total_Value", "type": 'numeric',"format": money}],            
            style_table={"overflowX": "auto"},
            id='data-grid'
    ),
    ],class_name='mb-3')
])
app.layout = dbc.Container([
    navbar,
    cd_layout
],className='dbc dbc-ag-grid',fluid=True)



@callback(
    Output('data-grid','data'),
    Input('principal','value'), 
    Input('rate','value'),
    Input('compound_n','value'),
    Input('compound_t','value'),
    Input('n_terms','value'),
    Input('reinvest_percent','value')

)
def generate_table(principal, rate, compound_n, compound_t, n_terms, reinvest_percent):
    df = hf.make_compound_reinvestment_df(principal,(rate/100),compound_n,compound_t,n_terms,percent_reinvest=reinvest_percent)
    return df.to_dict('records')

@callback(
    Output('data-chart','figure'),
    Input('principal','value'), 
    Input('rate','value'),
    Input('compound_n','value'),
    Input('compound_t','value'),
    Input('n_terms','value'),
    Input('reinvest_percent','value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")

)
def generate_chart(principal, rate, compound_n, compound_t, n_terms, reinvest_percent,toggle):
    template = LIGHT_THEME_TEMPLATE if toggle else DARK_THEME_TEMPLATE
    df = hf.make_compound_reinvestment_df(principal,(rate/100),compound_n,compound_t,n_terms,percent_reinvest=reinvest_percent)
    df = df.loc[:,['Term','Total_Value','Total_Interest']]
    df = pd.melt(df,id_vars='Term',var_name='Type')
    plt = px.line(df,x='Term',y='value',color="Type",template=template)
    return plt

@callback(
    Output('total-interest-callout','children'),
    Input('principal','value'), 
    Input('rate','value'),
    Input('compound_n','value'),
    Input('compound_t','value'),
    Input('n_terms','value'),
    Input('reinvest_percent','value')

)
def calculate_interest_earned(principal, rate, compound_n, compound_t, n_terms, reinvest_percent):
    df = hf.make_compound_reinvestment_df(principal,(rate/100),compound_n,compound_t,n_terms,percent_reinvest=reinvest_percent)
    total = float(df.iloc[[-1]]['Total_Interest'].iloc[0])
    text = f"${total:,.2f}"
    return text

# Run the app on port 8080
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8080, debug=True)
