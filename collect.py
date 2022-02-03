import fire
import json
import logging
import os
import numpy as np
import pandas as pd
from urllib.error import HTTPError

cwd = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=f'{cwd}/logs.log',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')


class Collection:
    def __init__(self):
        with open(f'config.json') as f:
            self.config = json.load(f)

    def get_url(self, year: int, week: int):
        """Formats url containing all seismic events in Iceland by week.

        Args:
            year (int): the desired year
            week (int): the desired week

        Returns:
            (str): the navigable url
        """
        url_raw = self.config['url']
        url = url_raw.replace('YEAR', str(year)).replace('WEEK', str(week))
        return url

    def scrape(self, url: str):
        """Scrapes the seismic data from the Icelandic MET's data service.

        Args:
            url (str): The url, containing the appropriate week and year

        Returns:
            (pd.DataFrame): A dataframe with all seismic events in Iceland
                in a single week

        Note:
            skipinitialspace=True is to circumvent the heterogenous spacing
                in the original document
        """
        try:
            return pd.read_csv(url, sep=' ', skipinitialspace=True, index_col=0)
        except HTTPError:
            logging.warning(
                'Scraping failed, ensure year/week combination exists')


def main(year=2021, week=10):

    collection_ = Collection()
    # sql = database.SQL()
    # for year in years:
    #     for week in weeks:
    url = collection_.get_url(year=year, week=week)
    data_by_week = collection_.scrape(url)
    print(data_by_week)
    # sql.write(table='seismicity', data=tabular_data, logging_message='earthquakes')


if __name__ == '__main__':
    fire.Fire(main)