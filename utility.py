from bank import Bank
import os
import sys
from definition import ROOT_PATH

PROJECT_ROOT = os.path.dirname(os.path.abspath(ROOT_PATH))
# Add the project root to the Python path
# sys.path.insert(0, PROJECT_ROOT)

bank_list_priv = [Bank(r'data_extraction/hdfc_slabs.csv', 'HDFC', 'HDFCBANK.NS'),
                  Bank(r'kotak_slabs.csv', 'KOTAK', 'KOTAKBANK.NS'),
                  Bank(r'data_extraction/icici_slabs.csv', 'ICICI', 'ICICIBANK.NS'),
                  Bank(r'data_extraction/axis_slabs.csv', 'AXIS', 'AXISBANK.NS'),
                  Bank(r'data_extraction/idfc_slabs.csv', 'IDFC', 'IDFCFIRSTB.NS')]

bank_list_public = [Bank(r'data_extraction/sbi_slabs.csv', 'SBI', 'SBIN.NS'),
                    Bank(r'data_extraction/pnb_slabs.csv', 'PNB', 'PNB.NS'),
                    Bank(r'data_extraction/bob_slabs.csv', 'BOB', 'BANKBARODA.NS'),
                    Bank(r'data_extraction/canara_slabs.csv', 'CANARA', 'CANBK.NS'),
                    Bank(r'data_extraction/union_slabs.csv', 'UNION', 'UNIONBANK.NS')]

master = bank_list_priv + bank_list_public

data = master[7].df
data.loc[7, 'Min Value'] = 271
data.loc[7, 'Max Value'] = 365


# bank_dict = {
#     'HDFC': Bank('https://www.paisabazaar.com/fixed-deposit/hdfc-fd-rates/'),
#     'AXIS': Bank('https://www.paisabazaar.com/fixed-deposit/axis-bank-fd-rates/'),
#     'ICICI': Bank('https://www.paisabazaar.com/fixed-deposit/icici-bank-fd-rates/'),
#     'IDFC': Bank('https://www.paisabazaar.com/idfc-bank/fixed-deposits/'),
#         }
