import pandas as pd


class CsvAction:
    @staticmethod
    def read_csv(name):
        data = pd.read_csv(name, error_bad_lines=False)
        return data
