import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from utility import master
from data_extraction.repo_rate import get_repo_rate
import numpy as np
import os
from datetime import date, datetime

# bucket_master = pd.read_csv('bucket_master.csv')
# repo_rate = get_repo_rate()
# fig_1 = px.line(bucket_master, x='Tenure', y='General Rate', color='Bank Name', markers=True)
# fig_1.add_hline(y=repo_rate, annotation_text=f'RBI Repo Rate {repo_rate}', annotation_position='top left')
#
# fig = make_subplots(rows=2, cols=2, subplot_titles=('AXIS', 'ICICI', 'HDFC', 'IDFC'))
#
# for bank in master:
#     bank.bucket_fig = px.line(bucket_master[bucket_master['Bank Name'] == bank.name], x='Tenure', y='General Rate',
#                               markers=True)
#     bank.bucket_fig.add_hline(y=repo_rate, annotation_text=f'RBI Repo Rate {repo_rate}', annotation_position='top left')
#
# fig.add_trace(
#     px.line(bucket_master[bucket_master['Bank Name'] == 'AXIS'], x='Tenure', y='General Rate', markers=True).data[0],
#     row=1, col=1)
# fig.add_trace(
#     px.line(bucket_master[bucket_master['Bank Name'] == 'ICICI'], x='Tenure', y='General Rate', markers=True).data[0],
#     row=1, col=2)
# fig.add_trace(
#     px.line(bucket_master[bucket_master['Bank Name'] == 'HDFC'], x='Tenure', y='General Rate', markers=True).data[0],
#     row=2, col=1)
# fig.add_trace(
#     px.line(bucket_master[bucket_master['Bank Name'] == 'IDFC'], x='Tenure', y='General Rate', markers=True).data[0],
#     row=2, col=2)
#
# fig.update_traces(line=dict(color='red'), row=1, col=1)
# fig.update_traces(line=dict(color='orange'), row=2, col=1)
# fig.update_traces(line=dict(color='green'), row=1, col=2)
# fig.update_traces(line=dict(color='purple'), row=2, col=2)
#
# fig.add_hline(y=repo_rate, row='all', col='all')
#
# # new_df = pd.DataFrame({'Bank': df.iloc[3650].index, 'Rate': df.iloc[3650].values})
# # fig = px.bar(new_df[new_df['Bank'].isin(['HDFC', 'PNB', 'SBI'])], x='Bank', y='Rate')
# # fig.update_layout(yaxis=dict(range=[5.0, 8.10], dtick=0.1))
# # fig.show()
#
# # REVENUE GRAPH
# df = pd.read_csv('bank_revenue.csv')
# df["TTM"] = df["TTM"].str.replace(",", "").astype(np.int64)
# df["Interest Income"] = df["Interest Income"].str.replace(",", "").astype(np.int64)
# df['Non Interest Income'] = df['TTM'] - df['Interest Income']
# df['Max Rate'] = None
# for bank in master:
#     df.loc[df['Bank Name'] == bank.name, 'Max Rate'] = bank.rate
# df.sort_values(by='TTM', inplace=True)
# # print(df)
# revenue_plot = px.bar(df, x='Bank Name', y=['Interest Income', 'Non Interest Income'],
#                       title='Interest Rate v/s Revenue', hover_data=['TTM', 'Max Rate'], text='Max Rate')

files = os.listdir('bank_historical_data')
historical_files = [file_name for file_name in files if file_name.startswith("historical")]
df_data = []


def get_date(filename):
    d = filename.split("_", 1)[1]
    d = d.replace("_", "-").replace('.csv', '')
    return d


def get_max_rates(filename):
    data = pd.read_csv(f'bank_historical_data/{filename}')
    max_rates = data.iloc[:, :].max()
    return max_rates


for file in historical_files:
    date = get_date(file)
    new_row = {
        'Date': date,
        'Filename': file,
    }
    new_row.update(get_max_rates(file))
    print(new_row)
    df_data.append(new_row)

df = pd.DataFrame(df_data)
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
df = df.sort_values(by='Date')
df = df.iloc[:, :-1]
target_date = "29-7-2023"
target_date = datetime.strptime(target_date, format('%d-%m-%Y'))
closest_date = min(df['Date'], key=lambda x: abs(x - target_date))
print(closest_date)
fig = px.line(df, x="Date", y=['HDFC', 'KOTAK'])
