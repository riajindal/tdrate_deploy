# DATA ANALYSIS TO BUCKET(SORT) SLABS
import pandas as pd
from data_analysis.bucket_slabs import bucket
from utility import bank_list_priv

# data = {
#     'HDFC': pd.read_csv(r'C:\Users\riaji\PycharmProjects\deposit_project\data_extraction\hdfc_slabs.csv'),
#     'ICICI': pd.read_csv(r'C:\Users\riaji\PycharmProjects\deposit_project\data_extraction\icici_slabs.csv'),
#     'AXIS': pd.read_csv(r'C:\Users\riaji\PycharmProjects\deposit_project\data_extraction\axis_slabs.csv'),
#     'IDFC': pd.read_csv(r'C:\Users\riaji\PycharmProjects\deposit_project\data_extraction\idfc_slabs.csv'),
# }

df_kotak = pd.read_csv(r'C:\Users\riaji\PycharmProjects\deposit_project\kotak_slabs.csv')
df_kotak.drop(columns=df_kotak.columns.difference(['Tenure', 'General Rate']), inplace=True)
df_kotak.loc[:, 'Bank Name'] = 'Kotak'
result = df_kotak

for bank in bank_list_priv:
    result = bucket(bank.name, bank.df, result)


