import pandas as pd
import plotly.express as px

df = pd.read_csv('sbi_historical_data.csv')
df['Effective Date'] = df['Effective Date'].loc[::-1].reset_index(drop=True)

fig = px.line(df, x='Effective Date', y='Interest Rate')
