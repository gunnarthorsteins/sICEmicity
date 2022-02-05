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
import plot

warnings.filterwarnings('ignore')
logging.basicConfig(filename=f'logs.log',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')

with open(f"config.json") as f:
    settings = json.load(f)
parameters = settings["default_values"]


def get_url(year: str, week: str):
    """Formats url containing all seismic events in Iceland by week.

    Args:
        year (str): %Y (i.e. four-digit) desired year
        week (str): zero-padded week number

    Returns:
        (str): the navigable url

    """

    with open(f'config.json') as f:
        config = json.load(f)
    url_raw = config['url']
    url = url_raw.replace('YEAR', year).replace('WEEK', week)
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


def filter(df: pd.DataFrame, x_min: float, x_max: float, y_min: float,
           y_max: float):
    """Removes seismic events outside desired bounding box

    Args:
        df (pd.DataFrame): The entire dataset
        x_min (float): Leftmost value
        x_max (float): Rightmost value
        y_min (float): Lowest value
        y_max (float): Highest value

    Returns:
        (pd.DataFrame): The filtered data
    """
    return df[(x_min < df.Lengd) & (df.Lengd < x_max) & (y_min < df.Breidd)
              & (df.Breidd < y_max)]


def parse_datetime(df: pd.DataFrame):
    df['Datetime'] = df['Dags.'].astype(str) + df['Timi'].astype(str)
    try:
        df['Datetime'] = pd.to_datetime(df['Datetime'],
                                        format=f'%Y%m%d%H%M%S.%f')
    except ValueError:
        logging.warning(
            'Parsing failed, probably due to time data not matching strformat')
    df.drop(['Dags.', 'Timi'], axis=1, inplace=True)
    return df


def main(**custom_params):
    for parameter, value in custom_params.items():
        parameters[parameter] = value

    # +1 b/c of Python's zero-based index
    years = np.arange(parameters['year_min'], parameters['year_max'] + 1)
    weeks = np.arange(parameters['week_min'], parameters['week_max'] + 1)
    for year in years:
        for week in weeks:
            if week < 10:
                week = f'0{week}'
            url = get_url(year=str(year), week=str(week))
            data_by_week = scrape(url)
            # data_filtered = filter(data_by_week,
            #                        x_min=parameters['x_min'],
            #                        x_max=parameters['x_max'],
            #                        y_min=parameters['y_min'],
            #                        y_max=parameters['y_max'])
            data_filtered_and_parsed = parse_datetime(data_by_week)
            logging.info(f'{year}-{week} scraped, filtered, and parsed')
            database.to_sql(df=data_filtered_and_parsed,
                            table_name='seismicity')


if __name__ == '__main__':
    fire.Fire(main)