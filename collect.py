# Note: I'm letting it fail on the current year if the week
# doesn't exist yet

import fire
import json
import logging
import os
import numpy as np
import pandas as pd
from urllib.error import HTTPError
import warnings

import database

warnings.filterwarnings('ignore')  # for pandas
logging.basicConfig(filename=f'logs.log',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')

with open(f"config.json") as f:
    settings = json.load(f)
parameters = settings["default_values"]


def get_url(year: int, week: int):
    """Formats url containing all seismic events in Iceland by week.

    Args:
        year (int): %Y (i.e. four-digit) desired year
        week (int): non-zero-padded week number

    Returns:
        (str): the navigable url

    """

    if week < 10:
        week = f'0{week}'

    with open(f'config.json') as f:
        config = json.load(f)
    url_raw = config['url']
    url = url_raw.replace('YEAR', str(year)).replace('WEEK', str(week))

    return url


def scrape(url: str):
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
        return pd.read_csv(url,
                           sep=' ',
                           skipinitialspace=True,
                           index_col=0,
                           dtype=str)
    except HTTPError:
        logging.warning('Scraping failed, ensure year/week combination exists')
        return None


def _compare(val: float, series: pd.Series):
    """Compares location values to edge of bbox.

    Helper function for filter().

    Args:
        val (float): The min/max value
        series (pd.Series): The lat/lon series of raw data

    Returns:
        (pd.Series): A series of booleans

    Note:
        .astype(float) b/c the df is scraped .astype(str). See Note in
        scrape() for why
    """
    return val < series.astype(float)


def filter(df: pd.DataFrame, bbox: dict):
    """Removes seismic events outside desired bounding box

    Args:
        df (pd.DataFrame): The entire dataset
        bbox (dict): A bounding box containing the following
            key-val pairs: x_min, x_max, y_min, y_max

    Returns:
        (pd.DataFrame): The filtered data
    """

    cond_1 = _compare(val=bbox['x_min'], series=df.Lengd)
    cond_2 = _compare(val=bbox['x_max'], series=df.Lengd)
    cond_3 = _compare(val=bbox['y_min'], series=df.Breidd)
    cond_4 = _compare(val=bbox['y_max'], series=df.Breidd)

    return df[cond_1 & cond_2 & cond_3 & cond_4]


def parse_datetime(df: pd.DataFrame):
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

    df['Datetime'] = df['Dags.'].astype(str) + df['Timi'].astype(str)
    try:
        df['Datetime'] = pd.to_datetime(df['Datetime'],
                                        format=f'%Y%m%d%H%M%S.%f')
    except KeyError or ValueError:
        logging.warning(
            'Parsing failed, probably due to time data not matching strformat')
    df.drop(['Dags.', 'Timi'], axis=1, inplace=True)

    return df


def main(**custom_params):
    """Collects seismic data from Icelandic MET by year and week.

    Usage:
        See google-fire docs.
    
    Example:
        $ python3 collect.py --year_min=2000 --year_max=2003
    """
    for parameter, value in custom_params.items():
        parameters[parameter] = value

    # +1 b/c of Python's zero-based index
    years = np.arange(parameters['year_min'], parameters['year_max'] + 1)
    weeks = np.arange(parameters['week_min'], parameters['week_max'] + 1)
    for year in years:
        for week in weeks:
            url = get_url(year=year, week=week)
            data_by_week = scrape(url)
            data_filtered_and_parsed = parse_datetime(data_by_week)
            logging.info(f'{year}-{week} scraped, filtered, and parsed')
            database.to_sql(df=data_filtered_and_parsed,
                            table_name='seismicity')


if __name__ == '__main__':
    fire.Fire(main)