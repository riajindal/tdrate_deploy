import os
import sys
import dash
import pandas as pd
import numpy as np
import plotly.express as px
from dash import html, dcc, callback, Input, Output
from utility import master
from definition import ROOT_PATH

PROJECT_ROOT = os.path.dirname(os.path.abspath(ROOT_PATH))
# Add the project root to the Python path
sys.path.insert(0, PROJECT_ROOT)

# Register page as a page on the dashboard
dash.register_page(__name__, path='/page-3', name='Day Wise Analysis')

# Define options to be displayed in dropdown
options = [{'label': bank.name, 'value': bank.name} for bank in master]
options.append({'label': 'ALL', 'value': 'all'})

# Create HTML page layout
layout = html.Div(id='div', children=[
    html.H2("Bank: Interest Rate v/s Revenue"),
    dcc.Dropdown(
        id='banks',
        options=options,
        optionHeight=35,
        value=['KOTAK', 'AXIS'],
        multi=True,
        clearable=True,
        style={'width': '50%'}
    ),
    dcc.Graph(id='revenue_graph', figure={}, style={'height': '800px'}),
])


# Callback function to add functionality to page
@callback(
    [Output(component_id='revenue_graph', component_property='figure')],
    [Input(component_id='div', component_property='children'),
     Input(component_id='banks', component_property='value')]
)
def update_graph(none, banks):

    df = pd.read_csv(r'bank_revenue.csv')
    df["TTM"] = df["TTM"].str.replace(",", "").astype(np.int64)
    df["Interest Income"] = df["Interest Income"].str.replace(",", "").astype(np.int64)
    df['Non Interest Income'] = df['TTM'] - df['Interest Income']
    df['Max Rate'] = None
    for bank in master:
        df.loc[df['Bank Name'] == bank.name, 'Max Rate'] = bank.rate
    df.sort_values(by='TTM', inplace=True)
    if 'all' not in banks:
        df = df[df["Bank Name"].isin(banks)]
    revenue_plot = px.bar(df, x='Bank Name', y=['Interest Income', 'Non Interest Income'],
                          title='Interest Rate v/s Revenue', hover_data=['TTM', 'Max Rate'], text='Max Rate')

    return [revenue_plot]
