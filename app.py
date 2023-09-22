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


cd_layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([dbc.Label("Principal"), dbc.Input(value = 20_000,id='principal', type='number')],width=6),
                dbc.Col([dbc.Label("Interest Rate"), dbc.Input(value = 4.25,id='rate', type='number')],width=6),
            ]),
            dbc.Row([
                dbc.Col([dbc.Label("Compound Periods per Year"), dbc.Input(value = 12,id='compound_n', type='number')],width=6),
                dbc.Col([dbc.Label("CD Length (years)"), dbc.Input(value = 0.75,id='compound_t', type='number')],width=6),
            ]),
            dbc.Row([
                dbc.Col([dbc.Label("Times Reinvested"), dbc.Input(value = 30,id='n_terms', type='number')],width=6),
                dbc.Col([dbc.Label("Reinvestment %"), dbc.Input(value = 100,id='reinvest_percent', type='number')],width=6),
            ])
        ],width=6, align='start'),
        dbc.Col([
            dcc.Graph(
                id='data-chart',

            )
        ],width=6, align='center')
    ]),
    dbc.Row([
        dag.AgGrid(
            defaultColDef={"resizable": True, "sortable": False, "filter": False},
            columnDefs=[
                {'field': 'Term'},
                {'field': "Term_Principal", "valueFormatter": {"function": "d3.format('($,.2f')(params.value)"}},
                {'field': "Term_Interest", "valueFormatter": {"function": "d3.format('($,.2f')(params.value)"}},
                {'field': "Total_Interest", "valueFormatter": {"function": "d3.format('($,.2f')(params.value)"}},
                {'field': "Total_Value", "valueFormatter": {"function": "d3.format('($,.2f')(params.value)"}},
            ],
            columnSize="sizeToFit",
            id='data-grid'
        )
    ])
])

app.layout = dbc.Container([
    html.H1(children="PyNance", style={'textAlign':'center'}),
    cd_layout
])



@callback(
    Output('data-grid','rowData'),
    Input('principal','value'), 
    Input('rate','value'),
    Input('compound_n','value'),
    Input('compound_t','value'),
    Input('n_terms','value'),
    Input('reinvest_percent','value')

)
def generate_table(principal, rate, compound_n, compound_t, n_terms, reinvest_percent):
    df = hf.make_compound_reinvestment_df(principal,(rate/100),compound_n,compound_t,n_terms,percent_reinvest=reinvest_percent)
    print(df)
    return df.to_dict('records')

@callback(
    Output('data-chart','figure'),
    Input('principal','value'), 
    Input('rate','value'),
    Input('compound_n','value'),
    Input('compound_t','value'),
    Input('n_terms','value'),
    Input('reinvest_percent','value')

)
def generate_chart(principal, rate, compound_n, compound_t, n_terms, reinvest_percent):
    df = hf.make_compound_reinvestment_df(principal,(rate/100),compound_n,compound_t,n_terms,percent_reinvest=reinvest_percent)
    df = df.loc[:,['Term','Total_Value','Total_Interest']]
    df = pd.melt(df,id_vars='Term',var_name='Type')
    plt = px.line(df,x='Term',y='value',color="Type",template='plotly_white')
    return plt

# Run the app on port 8080
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8080, debug=True)
