import math
import os
import sys
import dash
import pandas as pd
import plotly.express as px
from dash import html, dcc, callback, Input, Output
from plotly.subplots import make_subplots
from utility import master
from definition import ROOT_PATH

PROJECT_ROOT = os.path.dirname(os.path.abspath(ROOT_PATH))

# Add the project root to the Python path
sys.path.insert(0, PROJECT_ROOT)

# Register page as a page on the dashboard
dash.register_page(__name__, path='/', name='Home')

# Define options to be displayed in dropdown
options = [{'label': bank.name, 'value': bank.name} for bank in master]
options.append({'label': 'ALL', 'value': 'all'})

# Get repo rate from .txt file
with open('repo_rate.txt', 'r') as file:
    repo_rate = file.read()

# Create HTML page layout
layout = html.Div([
    html.H2("Tenure V/S Interest Rate"),
    dcc.Graph(id='tenure_graph', figure={}, className='mb-4'),
    html.H2("Individual Tenure Slabs V/S Interest Rate"),
    dcc.Dropdown(
        id='my_dropdown',
        options=options,
        optionHeight=35,
        value=['HDFC'],
        multi=True,
        clearable=True,
        style={'width': '50%'}
    ),
    dcc.Graph(id='indiv_graph', figure={}, style={'height': '800px'}),
])


# Callback function to add functionality to page
@callback(
    [Output(component_id='tenure_graph', component_property='figure'),
     Output(component_id='indiv_graph', component_property='figure')],
    [Input(component_id='my_dropdown', component_property='value')]
)
def update_graph(my_dropdown):
    bucket_master = pd.read_csv(r'bucket_master.csv')
    tenure_graph = px.line(bucket_master, x='Tenure', y='General Rate', color='Bank Name', markers=True)
    tenure_graph.add_hline(y=float(repo_rate), annotation_text=f'RBI Repo Rate {repo_rate}',
                           annotation_position='top left')

    for bank in master:
        bank.bucket_fig = px.line(bucket_master[bucket_master['Bank Name'] == bank.name], x='Tenure', y='General Rate',
                                  markers=True, title=bank.name)
        bank.bucket_fig.add_hline(y=float(repo_rate), annotation_text=f'RBI Repo Rate {repo_rate}',
                                  annotation_position='top left')
    figure_2 = ""
    if len(my_dropdown) == 1 and 'all' not in my_dropdown:
        for bank in master:
            if my_dropdown[0] == bank.name:
                figure_2 = bank.bucket_fig
    elif len(my_dropdown) > 1 and ('all' not in my_dropdown):
        row_count = math.ceil(len(my_dropdown) / 2)
        print(row_count)
        column_count = 2
        counter = 0
        figure_2 = make_subplots(rows=row_count, cols=column_count, subplot_titles=my_dropdown)
        for i in range(row_count):
            for j in range(column_count):
                if counter > len(my_dropdown) - 1:
                    break
                figure_2.add_trace(
                    px.line(bucket_master[bucket_master['Bank Name'] == my_dropdown[counter]], x='Tenure',
                            y='General Rate', markers=True, title=master[counter].name).data[0], row=i + 1, col=j + 1)
                counter += 1

    elif 'all' in my_dropdown:
        print('here')
        row_count = round(len(master) / 2)
        print(row_count)
        column_count = 2
        counter = 0
        figure_2 = make_subplots(rows=row_count, cols=column_count, subplot_titles=[bank.name for bank in master])
        for i in range(row_count):
            for j in range(column_count):
                if counter > len(master) - 1:
                    break
                figure_2.add_trace(
                    px.line(bucket_master[bucket_master['Bank Name'] == master[counter].name], x='Tenure',
                            y='General Rate', markers=True, title=master[counter].name).data[0], row=i + 1, col=j + 1)
                counter += 1
        figure_2.update_xaxes(showticklabels=False)

    counter = 0

    # indiv_plot.add_trace(
    #     px.line(bucket_master[bucket_master['Bank Name'] == 'AXIS'], x='Tenure', y='General Rate', markers=True).data[
    #         0], row=1, col=1)
    # indiv_plot.add_trace(
    #     px.line(bucket_master[bucket_master['Bank Name'] == 'ICICI'], x='Tenure', y='General Rate', markers=True).data[
    #         0], row=1, col=2)
    # indiv_plot.add_trace(
    #     px.line(bucket_master[bucket_master['Bank Name'] == 'HDFC'], x='Tenure', y='General Rate', markers=True).data[
    #         0], row=2, col=1)
    # indiv_plot.add_trace(
    #     px.line(bucket_master[bucket_master['Bank Name'] == 'IDFC'], x='Tenure', y='General Rate', markers=True).data[
    #         0], row=2, col=2)
    #
    # indiv_plot.update_traces(line=dict(color='red'), row=1, col=1)
    # indiv_plot.update_traces(line=dict(color='orange'), row=2, col=1)
    # indiv_plot.update_traces(line=dict(color='green'), row=1, col=2)
    # indiv_plot.update_traces(line=dict(color='purple'), row=2, col=2)
    #
    figure_2.add_hline(y=float(repo_rate), row='all', col='all', annotation_text=f'RBI Repo Rate {repo_rate}',
                       annotation_position='top left')
    #
    # if my_dropdown != 'all':
    #     for bank in master:
    #         if my_dropdown == bank.name:
    #             indiv_plot = bank.bucket_fig

    return tenure_graph, figure_2
