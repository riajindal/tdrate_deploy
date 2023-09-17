import os
import sys
import pandas as pd
from utility import master
from datetime import datetime, timedelta, date
from definition import ROOT_PATH

PROJECT_ROOT = os.path.dirname(os.path.abspath(ROOT_PATH))
# Add the project root to the Python path
# for saving and running files in appropriate directories
sys.path.insert(0, PROJECT_ROOT)
print(os.getcwd())

# Create data frame to store interest rates data for
# the current date with rows from 1 to 3650 and
# columns being each bank studied
today = date.today()
df = pd.DataFrame(index=list(range(3651)))
for bank in master:
    df[bank.name] = 'None'
    for index, row in bank.df.iterrows():
        min = row['Min Value']
        max = row['Max Value']
        # print(index)
        for i in range(min, max + 1):
            # print(df[bank_list[0].name].loc[i])
            df.loc[i, bank.name] = bank.df.at[index, 'General Rate']

# Conditional logic to only save created data frame
# if it is different from the last stored historical .csv
# file in order to save memory usage
directory = "bank_historical_data/"
curr_files = [(file, os.path.getctime(os.path.join(directory, file))) for file in os.listdir("bank_historical_data")]
curr_files = sorted(curr_files, key=lambda x: x[1], reverse=True)
df_to_compare = pd.read_csv(f'bank_historical_data/{curr_files[0][0]}')
df_to_compare = df_to_compare.fillna(value='None')
if df.equals(df_to_compare):
    exit()
else:
    filename = r'bank_historical_data/historical_' + str(today.day) + '_' + str(today.month) + '_' + str(today.year) + '.csv '
    df.to_csv(filename, mode='w', index=False)
    print(filename)
