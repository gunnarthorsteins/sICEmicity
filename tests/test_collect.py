import json
import os
import sys
import unittest
from urllib.error import HTTPError

import pandas as pd

# To import from other parent directory in repo
pwd = os.getcwd()
sys.path.insert(0, pwd)

import collect

with open(f"config.json") as f:
    settings = json.load(f)
bbox = settings["default_values"]

YEAR = 2021
WEEK = 10
url_val = f'http://hraun.vedur.is/ja/viku/{YEAR}/vika_{WEEK}/listi'


def get_validation_csv():
    return pd.read_csv(f'tests/test_files/{YEAR}-{WEEK}.csv',
                       sep=' ',
                       skipinitialspace=True,
                       index_col=0,
                       dtype=str)


class TestCollect(unittest.TestCase):

    def test_url(self):
        url = collect.get_url(year=YEAR, week=WEEK)
        self.assertEqual(url, url_val)

    def test_scraping(self):
        df_val = get_validation_csv()
        df_test = collect.scrape(url_val)
        pd.testing.assert_frame_equal(df_test, df_val)

    def test_scraping_exception(self):
        '''Create a broken url'''
        broken_url = f'{url_val}f'
        df = collect.scrape(broken_url)
        self.assertIsNone(df)

    def test_filter(self):
        df_val = get_validation_csv()
        df_filtered = collect.filter(df_val, bbox=bbox)
        self.assertNotEqual(len(df_val), len(df_filtered))
        self.assertIsNotNone(df_filtered)

    def test_datetime_parsing(self):
        df_val = get_validation_csv()
        cols_val = df_val.columns
        df_parsed_datetime = collect.parse_datetime(df_val)
        parsed_columns = df_parsed_datetime.columns
        self.assertNotEqual(len(parsed_columns), len(cols_val))
        self.assertIn('Datetime', parsed_columns)
        self.assertNotIn('Timi', parsed_columns)

    def test_datetime_parsing_exception(self):
        df_faulty = pd.read_csv('tests/test_files/faulty_file.csv')
        self.assertRaises(KeyError, collect.parse_datetime, df_faulty)


if __name__ == '__main__':
    unittest.main()