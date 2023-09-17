import os
import sys
import dash
import pandas as pd
import plotly.express as px
from dash import html, dcc, callback, Input, Output
from datetime import date, datetime
from utility import master
from definition import ROOT_PATH

PROJECT_ROOT = os.path.dirname(os.path.abspath(ROOT_PATH))
# Add the project root to the Python path
sys.path.insert(0, PROJECT_ROOT)

# Register page as a page on the dashboard
dash.register_page(__name__, path='/page-4', name='Historical Analysis')

# Define options to be displayed in dropdown
options = [{'label': bank.name, 'value': bank.name} for bank in master]
options.append({'label': 'ALL', 'value': 'all'})

# Create HTML page layout
layout = html.Div(id='div', children=[
    html.H2("Historical Trend Analysis"),
    dcc.DatePickerRange(
        id='selected_date',
        min_date_allowed=date(2023, 7, 21),
        max_date_allowed=date.today(),
        initial_visible_month=date(2023, 7, 21),
        start_date=date(2023, 7, 21),
        end_date=date.today(),
    ),
    dcc.Dropdown(
        id='banks',
        options=options,
        optionHeight=35,
        value=['KOTAK', 'AXIS'],
        multi=True,
        clearable=True,
        style={'width': '50%'}
    ),
    dcc.Graph(id='historical_graph', figure={}, style={'height': '800px'}),
])


# Callback function to add functionality to page
@callback(
    [Output(component_id='historical_graph', component_property='figure')],
    [Input(component_id='div', component_property='children'),
     Input(component_id='selected_date', component_property='start_date'),
     Input(component_id='selected_date', component_property='end_date'),
     Input(component_id='banks', component_property='value')]
)
def update_graph(none, start_date, end_date, banks):
    files = os.listdir('bank_historical_data')
    historical_files = [file_name for file_name in files if file_name.startswith("historical")]
    df_data = []

    # Get date from .csv file name
    def get_date(filename):
        d = filename.split("_", 1)[1]
        d = d.replace("_", "-").replace('.csv', '')
        return d

    # Get the max rate for a date to plot in the
    # form of an array of the max values for each bank
    def get_max_rates(filename):
        data = pd.read_csv(f'bank_historical_data/{filename}')
        max_rates = data.iloc[:, :].max()
        return max_rates

    # Convert date from string to datetime format
    # for further manipulation and usage
    def format_date(value):
        res = datetime.strptime(value, "%Y-%m-%d")
        res = datetime.strftime(res, "%d-%m-%Y")
        res = pd.to_datetime(res, dayfirst=True)
        return res

    # Get the closest .csv file matching the input date
    def get_closest_date(value):
        return min(df['Date'], key=lambda x: abs(x - value))

    # Get dates as strings from historical files
    for file in historical_files:
        date = get_date(file)
        new_row = {
            'Date': date,
            'Filename': file,
        }
        new_row.update(get_max_rates(file))
        df_data.append(new_row)

    # Create a new data frame to store
    # dates and respective Max Values to plot
    # Format:- {'Date', 'Filename', ... (each bank name)}
    # Here df['HDFC'] for instance would store that
    # dates max HDFC interest rate
    df = pd.DataFrame(df_data)
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    df = df.sort_values(by='Date')

    start_date = format_date(start_date)
    end_date = format_date(end_date)

    start_date = get_closest_date(start_date)
    end_date = get_closest_date(end_date)

    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    fig = px.line(df, x="Date", y=banks)

    return [fig]
