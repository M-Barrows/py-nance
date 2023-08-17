# app.py
# This is the main file for the Dash app

# Import the necessary modules
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MORPH])
app.title = 'Py-Nance'

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink('CDs', href='/cds'))
    ],
    brand='Py-Nance',
    brand_href='/',
    color='primary',
    dark=True,
    fluid=True
)

footer = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.P([
                'Made with ',
                html.Span('❤️', className='text-danger'),
                ' by ',
                html.A('Code and Coffee', href='https://blog.codecoffee.org', target='_blank')
            ], className='text-center')
        )
    ),
    fluid=True,
    className='fixed-bottom bg-light'
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    dbc.Container(id='page-content', fluid=True),
    footer
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/cds':
        return cds_layout
    else:
        return main_layout

main_layout = dbc.Container([
    dbc.Container([
        html.H1('Py-Nance', className='display-3 text-center'),
        html.P(
            'A collection of open-source tools to help you understand your financial future and answer some of the "what if?" questions.',
            className='lead text-center'
        ),
        html.Hr(className='my-2'),
        dbc.Row([
            dbc.Col([
                html.A(
                dbc.Card([
                    dbc.CardImg(src='/assets/cd.png', top=True),
                    dbc.CardBody([
                        html.H4('How much will your CD be worth?', className='card-title')
                    ])
                ]), href="/cds")
            ], width=6),

        ])
    ])
], fluid=True)

cds_layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Label('APY:'), width=2),
        dbc.Col(dcc.Input(id='apy', type='number', min=0, step=0.01), width=4)
    ]),
    dbc.Row([
        dbc.Col(html.Label('Term Length (months):'), width=2),
        dbc.Col(dcc.Input(id='term_length', type='number', min=0, step=1), width=4)
    ]),
    dbc.Row([
        dbc.Col(html.Label('Starting Value:'), width=2),
        dbc.Col(dcc.Input(id='starting_value', type='number', min=0, step=0.01), width=4)
    ]),
    html.Br(),
    html.Div(id='output')
], fluid=True)

@app.callback(
    Output('output', 'children'),
    [Input('apy', 'value'), Input('term_length', 'value'), Input('starting_value', 'value')]
)
def calculate_final_value(apy, term_length, starting_value):
    if apy is not None and term_length is not None and starting_value is not None:
        final_value = starting_value * (1 + apy/100) ** (term_length/12)
        return f'Final Value: ${final_value:,.2f}'
    else:
        return 'Please enter values for APY, term length, and starting value.'

# Run the app on port 8080
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8080, debug=True)
