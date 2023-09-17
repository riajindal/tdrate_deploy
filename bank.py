import pandas as pd


class Bank:

    def __init__(self, csv, bank_name, code):
        self.csv_path = csv
        self.name = bank_name
        self.df = pd.read_csv(csv)
        self.rate = self.get_highest_rate()
        self.id = code

    def get_highest_rate(self):
        return self.df['General Rate'].max()

