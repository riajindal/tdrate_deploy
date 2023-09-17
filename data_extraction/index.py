# DATA EXTRACTION DRIVER FILE
from extract_slabs import create_csv

# banks = icici, hdfc, idfc, axis
# store in dictionary: {'bank name': 'url'}
urls_private = {
    'HDFC': 'https://www.paisabazaar.com/fixed-deposit/hdfc-fd-rates/',
    'KOTAK': 'https://www.paisabazaar.com/fixed-deposit/kotak-mahindra-bank-fd-rates/',
    'AXIS': 'https://www.paisabazaar.com/fixed-deposit/axis-bank-fd-rates/',
    'ICICI': 'https://www.paisabazaar.com/fixed-deposit/icici-bank-fd-rates/',
    'IDFC': 'https://www.paisabazaar.com/idfc-bank/fixed-deposits/',
        }

urls_public = {
    'SBI': 'https://www.paisabazaar.com/fixed-deposit/sbi-fd-rates/',
    'PNB': 'https://www.paisabazaar.com/fixed-deposit/pnb-fd-rates/',
    'BOB': 'https://www.paisabazaar.com/fixed-deposit/bank-of-baroda-fd-rates/',
    'CANARA': 'https://www.paisabazaar.com/fixed-deposit/canara-bank-fd-rates/',
    'UNION': 'https://www.paisabazaar.com/union-bank-of-india/fixed-deposits/'
}

for key, value in urls_private.items():
    create_csv(key, value)

for key, value in urls_public.items():
    create_csv(key, value)

# print(bank_dict['HDFC'].df)
