import os
import sys
import dash
import pandas as pd
import plotly.express as px
from dash import html, dcc, callback, Input, Output
from data_analysis.compare_rates import df
from definition import ROOT_PATH

PROJECT_ROOT = os.path.dirname(os.path.abspath(ROOT_PATH))

# Add the project root to the Python path
sys.path.insert(0, PROJECT_ROOT)

# Add the project root to the Python path
dash.register_page(__name__, path='/page-2', name='Day Wise Analysis')

# Get repo rate from .txt file
with open('repo_rate.txt', 'r') as file:
    repo_rate = float(file.read())

# Create HTML page layout
layout = html.Div([
    html.H2('Interest Rate Comparison'),
    dcc.Input(id='day', value='7', type='number', min=7, max=3650, step=1, debounce=True, className="my-2"),
    html.Br(),
    dcc.Dropdown(
        id='compare_dropdown',
        options=[
            {'label': 'HDFC Bank', 'value': 'HDFC'},
            {'label': 'KOTAK Bank', 'value': 'KOTAK'},
            {'label': 'ICICI Bank', 'value': 'ICICI'},
            {'label': 'Axis Bank', 'value': 'AXIS'},
            {'label': 'IDFC Bank', 'value': 'IDFC'},
            {'label': 'SBI Bank', 'value': 'SBI'},
            {'label': 'PNB Bank', 'value': 'PNB'},
            {'label': 'CANARA Bank', 'value': 'CANARA'},
            {'label': 'UNION Bank', 'value': 'UNION'},
            {'label': 'BARODA Bank', 'value': 'BOB'},
            {'label': 'All', 'value': 'all'}
        ],
        multi=True,
        optionHeight=35,
        value=['KOTAK', 'SBI'],
        clearable=True,
        style={'width': '50%'}
    ),
    dcc.Graph(id='m', figure={}),
])


# Callback function to add functionality to page
@callback(
    [Output(component_id='m', component_property='figure')],
    [Input(component_id='day', component_property='value'),
     Input(component_id='compare_dropdown', component_property='value')]
)
def update_graph(day, compare_dropdown):
    new_df = pd.DataFrame({'Bank': df.iloc[int(day)].index, 'Rate': df.iloc[int(day)].values})
    if 'all' in compare_dropdown:
        compare_dropdown = new_df['Bank']
    figure_4 = px.bar(new_df[new_df['Bank'].isin(compare_dropdown)], x='Bank', y='Rate')
    figure_4.add_hline(y=6.5, annotation_text=f'RBI Repo Rate {repo_rate}', annotation_position='top left')
    figure_4.update_layout(yaxis=dict(range=[2.0, 8.10], dtick=2.0))

    return [figure_4]
