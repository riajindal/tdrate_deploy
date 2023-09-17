import dash
import pandas as pd
from data_analysis.compare_rates import df
import plotly.express as px
from dash import html, dcc, Input, Output
import socket
from tenure_rates import fig as rate_plot
from comp_interest_rate_plot import fig_1 as tenure_plot
from comp_interest_rate_plot import fig as indiv_plot
from utility import master
from comp_interest_rate_plot import repo_rate, revenue_plot

# Dashboard:-

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Fixed Deposit Dashboard", style={'textAlign': 'center'}),
    html.Div(id='none', children=[]),
    dcc.Graph(id='my_bar_chart', figure={}),
    html.H2("Tenure Slabs V/S Interest Rate"),
    dcc.Graph(id='tenure_graph', figure={}),
    html.H2("Individual Tenure Slabs V/S Interest Rate"),
    dcc.Dropdown(
        id='my_dropdown',
        options=[
            {'label': 'HDFC Bank', 'value': 'HDFC'},
            {'label': 'ICICI Bank', 'value': 'ICICI'},
            {'label': 'Axis Bank', 'value': 'AXIS'},
            {'label': 'IDFC Bank', 'value': 'IDFC'},
            {'label': 'All', 'value': 'all'}
        ],
        optionHeight=35,
        value='HDFC',
        multi=False,
        clearable=True,
        style={'width': '50%'}
    ),
    dcc.Graph(id='indiv_graph', figure={}, style={'height': '800px'}),
    html.H2('Interest Rate Comparison'),
    dcc.Input(id='day', value='7', type='number', min=7, max=3650, step=1, debounce=True),
    dcc.Dropdown(
        id='compare_dropdown',
        options=[
            {'label': 'HDFC Bank', 'value': 'HDFC'},
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
        value=['HDFC', 'SBI'],
        clearable=True,
        style={'width': '50%'}
    ),
    dcc.Graph(id='m', figure={}),
    html.H2("Bank: Interest Rate v/s Revenue"),
    dcc.Graph(id='revenue_graph', figure={}, style={'height': '800px'}),
])


@app.callback(
    [Output(component_id='my_bar_chart', component_property='figure'),
     Output(component_id='tenure_graph', component_property='figure'),
     Output(component_id='indiv_graph', component_property='figure'),
     Output(component_id='m', component_property='figure'),
     Output(component_id='revenue_graph', component_property='figure')],
    [Input(component_id='none', component_property='children'),
     Input(component_id='my_dropdown', component_property='value'),
     Input(component_id='day', component_property='value'),
     Input(component_id='compare_dropdown', component_property='value')]
)
def update_graph(none, my_dropdown, day, compare_dropdown):
    figure_1 = rate_plot

    figure_2 = tenure_plot

    if my_dropdown == 'all':
        figure_3 = indiv_plot
    else:
        for bank in master:
            if my_dropdown == bank.name:
                figure_3 = bank.bucket_fig

    new_df = pd.DataFrame({'Bank': df.iloc[int(day)].index, 'Rate': df.iloc[int(day)].values})
    if 'all' in compare_dropdown:
        compare_dropdown = new_df['Bank']
    figure_4 = px.bar(new_df[new_df['Bank'].isin(compare_dropdown)], x='Bank', y='Rate')
    figure_4.add_hline(y=repo_rate, annotation_text=f'RBI Repo Rate {repo_rate}', annotation_position='top left')
    figure_4.update_layout(yaxis=dict(range=[2.0, 8.10], dtick=2.0))

    figure_5 = revenue_plot

    return figure_1, figure_2, figure_3, figure_4, figure_5


def find_available_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))  # Bind to a random available port
    _, port = sock.getsockname()
    sock.close()
    return port


# Usage
port = find_available_port()
print(f"Available port: {port}")

# Use the port variable in your Dash app configuration
app.run_server(debug=True, port=port)
