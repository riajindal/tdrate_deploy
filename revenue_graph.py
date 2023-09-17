import plotly.express as px
from utility import master
import pandas as pd
import numpy as np

df = pd.read_csv('bank_revenue.csv')
df["TTM"] = df["TTM"].str.replace(",", "").astype(np.int64)
df["Interest Income"] = df["Interest Income"].str.replace(",", "").astype(np.int64)
df['Non Interest Income'] = df['TTM'] - df['Interest Income']
df['Max Rate'] = None
for bank in master:
    df.loc[df['Bank Name'] == bank.name, 'Max Rate'] = bank.rate
df.sort_values(by='TTM', inplace=True)
print(df)
fig = px.bar(df, x='Bank Name', y=['Interest Income', 'Non Interest Income'], title='Interest Rate v/s Revenue', hover_data=['TTM', 'Max Rate'], text='Max Rate')
fig.show()
