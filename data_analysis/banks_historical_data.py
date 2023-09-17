import pandas as pd
from datetime import datetime, timedelta, date
from utility import master

# STARTER CODE TO CREATE INITIAL CSV
# start_date = datetime(2023, 7, 20)
# end_date = datetime.now()
#
# date_range = pd.date_range(start=start_date, end=end_date, freq='D')
#
# df = pd.DataFrame(columns=(['Date', 'Tenure'] + [bank.name for bank in master]))
#
# while start_date < end_date:
#     for bank in master:
#         for index, row in bank.df.iterrows():
#             new_row = {
#                 'Date': start_date,
#                 'Tenure': bank.df.loc[index, 'Tenure'],
#                 bank.name: bank.df.loc[index, 'General Rate']
#             }
#             df.loc[len(df)] = new_row
#     start_date += timedelta(days=1)
#
# df.to_csv('banks_historical_1.csv', mode='w', index=False)


# CODE TO APPEND INFORMATION
# data = []
# banks_historical = pd.read_csv('banks_historical.csv')
# start_date = banks_historical['Date'].iloc[-1]
# start_date = datetime.strptime(start_date, '%Y-%m-%d')
# start_date = date(start_date.year, start_date.month, start_date.day)
# current_date = date.today()
#
# while start_date < current_date:
#     start_date += timedelta(days=1)
#     new_row = {'Date': start_date.strftime('%Y-%m-%d')}
#     for bank in master:
#         new_row[bank.name] = bank.rate
#     data.append(new_row)
#
# df = pd.DataFrame(data)
#
# df.to_csv('banks_historical.csv', mode='a', header=False, index=False)

try:
    with open('banks_historical_1.csv') as f:
        df = pd.read_csv(f)
        start_date = df['Date'].iloc[-1]
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        start_date = date(start_date.year, start_date.month, start_date.day)
        end_date = date.today()
        new_df = pd.DataFrame(columns=(['Date', 'Tenure'] + [bank.name for bank in master]))
        while start_date < end_date:
            start_date += timedelta(days=1)
            for bank in master:
                for index, row in bank.df.iterrows():
                    new_row = {
                        'Date': start_date,
                        'Tenure': bank.df.loc[index, 'Tenure'],
                        bank.name: bank.df.loc[index, 'General Rate']
                    }
                    new_df.loc[len(new_df)] = new_row

        new_df.to_csv('banks_historical_1.csv', mode='a', header=False, index=False)

except FileNotFoundError:
    start_date = date(2023, 7, 20)
    end_date = date.today()

    date_range = pd.date_range(start=start_date, end=end_date, freq='D')

    df = pd.DataFrame(columns=(['Date', 'Tenure'] + [bank.name for bank in master]))

    while start_date < end_date:
        for bank in master:
            for index, row in bank.df.iterrows():
                new_row = {
                    'Date': start_date,
                    'Tenure': bank.df.loc[index, 'Tenure'],
                    bank.name: bank.df.loc[index, 'General Rate']
                }
                df.loc[len(df)] = new_row
        start_date += timedelta(days=1)

    df.to_csv(f'data_analysis/banks_historical_1.csv', mode='w', index=False)


