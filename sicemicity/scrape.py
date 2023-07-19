from dataclasses import dataclass
from functools import reduce
import json
import logging
from typing import Callable
from urllib.error import HTTPError

import pandas as pd

from sicemicity import database


with open('config.json') as f:
    config = json.load(f)

url = config['url']
dt_col = 'datetime'


@dataclass
class YearWeek:
    year: str|int
    week: str|int

    def table(self):
        return f'{self.year}-{self.week}'

    def url(self) -> str:
        """Formats url containing all seismic events in Iceland by week.

        Args:
            year (int): %Y (i.e. four-digit) desired year
            week (int): non-zero-padded week number

        Returns:
            (str): the navigable url
        """

        if int(self.week) < 10:    
            self.week = f'0{self.week}'

        return url.replace('YEAR', str(self.year)).replace('WEEK', str(self.week))


def _scrape(url: str) -> pd.DataFrame|None:
    """Scrapes the seismic data from the Icelandic MET's data service.

    Args:
        url (str): The url, containing the appropriate week and year

    Returns:
        (pd.DataFrame): A dataframe with all seismic events in Iceland
            in a single week

    Note:
        skipinitialspace=True is to circumvent the heterogenous spacing
            in the original document
        dtype=str is to handle edge case where leading time digits are 0.
           Otherwise it omits these zero(s)
    """

    try:
        print(url)
        return pd.read_csv(
            url,
            sep=' ',
            skipinitialspace=True,
            index_col=0,
            dtype=str
        )

    except HTTPError:
        logging.warning('Scraping failed, ensure year/week combination exists')


def parse_datetime(seismicity: pd.DataFrame) -> pd.DataFrame:
    """Parses datetime info to a SQL-friendly format.
    
    The original document contains two separate date and time columns.
    This method merges the two.
    
    Args:
        df (pd.DataFrame): A raw dataframe of the original document

    Returns:
        (pd.DataFrame): A dataframe with a parsed datetime column

    Raises:
        KeyError: When the original file is improperly formatted.
            It's rare though (~.2%). In that case those files must be
            manually downloaded and parsed with faulty_files.py
    """
    print(seismicity.info())

    seismicity[dt_col] = seismicity['Dags.'].astype(str) + seismicity['Timi'].astype(str)
    
    try:
        seismicity[dt_col] = pd.to_datetime(
            seismicity[dt_col],
            format='%Y%m%d%H%M%S.%f'
        )

    except KeyError or ValueError:
        logging.warning(
            'Parsing failed, probably due to time data not matching strformat'
        )
        
    seismicity.drop(['Dags.', 'Timi'], axis=1, inplace=True)

    return seismicity


def scrape(year, week) -> None:
    yearweek = YearWeek(year=year, week=week)
    fns: tuple[Callable, ...] = (_scrape, parse_datetime)
    seismicity = reduce(lambda x, fn: fn(x), fns, yearweek.url())  # Functionaaaaaal

    logging.info(f'{yearweek} scraped, filtered, and parsed')
    database.write(df=seismicity, table_name=yearweek.table())