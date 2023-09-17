import pandas as pd
import os
import sys
from collections import defaultdict
from definition import ROOT_PATH

PROJECT_ROOT = os.path.dirname(os.path.abspath(ROOT_PATH))
sys.path.insert(0, PROJECT_ROOT)

# def convert_to_days(duration):
#     days = 0
#     if duration is None:
#         return 0
#     flag = re.findall(r"less than", duration)
#     matches = re.findall(r'(\d+)\s*(days?|months?|years?)', duration, re.IGNORECASE)
#     for match in matches:
#         value, unit = match
#         if unit.lower() in ['day', 'days']:
#             days += int(value)
#         elif unit.lower() in ['month', 'months']:
#             days += int(value) * 30  # Assuming 30 days in a month
#         elif unit.lower() in ['year', 'years']:
#             days += int(value) * 365  # Assuming 365 days in a year
#             if flag:
#                 days -= 1
#
#     if not matches:
#         try:
#             days += int(duration)
#         except ValueError:
#             pass
#
#     return days


def bucket(bank_name, df):
    df_kotak = pd.read_csv(r'kotak_slabs.csv')
    # CUSTOM BUCKETING FUNCTION

    def bucket_slabs(df_1, df_2):
        # Starting columns to easily view slabs
        # and how to bucket them
        # result = pd.concat([df_2['Min Value'], df_1['Min Value'], df_1['Max Value']], axis=1)
        # print(result)

        # Creating list component of columns
        # Min Value and Tenure for easy iteration
        bank_2 = df_2['Min Value'].tolist()
        bank_2_ranges = df_2['Tenure'].tolist()

        bank_1_min = df_1['Min Value'].tolist()
        bank_1_max = df_1['Max Value'].tolist()
        ranges = df_1['Tenure'].tolist()

        # Dictionary to store binned values
        # as key value pairs in the format
        # key: Bank Range to be binned
        # value: Bank Range to be binned into (Kotak)
        binned_range = {}

        for i in range(max(len(bank_2), len(bank_1_min))):
            if i >= len(bank_2):
                break
            if i < len(bank_1_min) and (
                    bank_1_min[i] <= bank_2[i] < bank_1_max[i] or abs(bank_1_min[i] - bank_2[i]) <= 3):
                # print(kotak_min[i], icici[i])
                binned_range[bank_2_ranges[i]] = ranges[i]
            else:
                condition = True
                if i >= len(bank_1_min):
                    c = len(bank_1_min) - 1
                else:
                    c = i - 1
                while condition:
                    if bank_1_min[c] <= bank_2[i] < bank_1_max[c] or abs(bank_1_min[c] - bank_2[i]) <= 3:
                        # print(kotak_min[c], icici[i])
                        binned_range[bank_2_ranges[i]] = ranges[c]
                        condition = False
                    c -= 1

        return binned_range

    binned = bucket_slabs(df_kotak, df)

    # Custom function to get average interest after binning
    def get_average_interest(binned, df_1):
        res = defaultdict(list)

        # Reversing the key value pairs for
        # each Kotak bin as key to have a
        # list as value containing all the
        # ranges that fall into it
        for key, value in binned.items():
            res[value].append(key)

        # Replacing the tenure range with the corresponding
        # interest rate and for multiple slabs in one bucket
        # taking an average value of the rates
        for key, values in res.items():
            res[key] = [df_1.loc[df_1['Tenure'] == value, 'General Rate'].values[0] for value in values]

        for key, value in res.items():
            average_value = sum(value) / len(value)
            res[key] = round(average_value, 2)

        return res

    # print(binned)

    res = get_average_interest(binned, df)

    # Updating the Kotak Data Frame to include only
    # relevant columns i.e. Tenure, General Rate, Bank Name
    df_kotak.drop(columns=df_kotak.columns.difference(['Tenure', 'General Rate']), inplace=True)
    df_kotak.loc[:, 'Bank Name'] = 'Kotak'

    df = pd.DataFrame(list(res.items()), columns=['Tenure', 'General Rate'])
    df.loc[:, 'Bank Name'] = bank_name

    # Creating a final data frame containing the
    # bucketed slabs, interest rates and original buckets
    # and adding them to a resultant storage structure
    # which can be plotted

    # df structure = {['Tenure, 'General Rate', 'Bank Name']}
    # def add_bank_slabs(binned_slabs, bank_name, main):
    #     df = pd.DataFrame(list(binned_slabs.items()), columns=['Tenure', 'General Rate'])
    #     df.loc[:, 'Bank Name'] = bank_name
    #     main = pd.concat([main, df], axis=0, ignore_index=True)
    #     del df
    #     return main
    #
    # main = add_bank_slabs(res, bank_name, main)

    return df
    # print(result.tail())


# print(os.getcwd())
