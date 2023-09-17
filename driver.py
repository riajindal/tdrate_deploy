import subprocess
import pandas as pd
from utility import master
from data_analysis.bucket_slabs import bucket
from data_extraction.repo_rate import get_repo_rate
import os
from definition import ROOT_PATH

PROJECT_ROOT = os.path.dirname(os.path.abspath(ROOT_PATH))

# print(os.getcwd())

# Extract data from PaisaBazaar website in respective directory i.e. data_extraction
subprocess.run(['python', r'data_extraction/index.py'])

# Create bucketed data master sheet
# 1. Create general format for bucket_master.csv
df_kotak = pd.read_csv(r'kotak_slabs.csv')
df_kotak.drop(columns=df_kotak.columns.difference(['Tenure', 'General Rate']), inplace=True)
df_kotak.loc[:, 'Bank Name'] = 'Kotak'

# 2. Get buckets for each bank
for bank in master:
    bank.bucket_df = bucket(bank.name, bank.df)

# 3. Concatenate each banks bucketed dataframe to bucket_master.csv
bucket_master = df_kotak
for bank in master:
    bucket_master = pd.concat([bucket_master, bank.bucket_df], axis=0, ignore_index=True)

# 4. Store as .csv file
bucket_master.to_csv('bucket_master.csv', mode='w', index=False)

# Extract bank historical data for future use
# subprocess.run(['python', r'data_analysis\banks_historical_data.py'])
subprocess.run(['python', r'bank_historical_data/extract_historical.py'])

# Revenue Extraction from Yahoo Financials
subprocess.run(['python', r'extract_revenue.py'])

# Extract RBI Repo Rate and store as .txt file for quick access
repo_rate = str(get_repo_rate())
with open('repo_rate.txt', 'w+') as file:
    file.write(repo_rate)

