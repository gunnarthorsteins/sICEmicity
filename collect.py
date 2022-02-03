# Note: I'm letting it fail on the current year if the week
# hasn't passed yet

import fire
import json
import logging
import os
import numpy as np
import pandas as pd
from urllib.error import HTTPError

# To call from crontab
cwd = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=f'{cwd}/logs.log',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')

with open("config.json") as f:
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
    """

    try:
        return pd.read_csv(url, sep=' ', skipinitialspace=True, index_col=0)
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


def collect(**custom_params):
    for parameter, value in custom_params.items():
        parameters[parameter] = value

    # +1 b/c of Python's zero-based index
    years = np.arange(parameters['year_min'] + 1, parameters['year_max'] + 1)
    weeks = np.arange(1, 53)
    # sql = database.SQL()
    for year in years:
        for week in weeks:
            if week < 10:
                week = f'0{week}'
            url = get_url(year=str(year), week=str(week))
            data_by_week = scrape(url)
            data_filtered = filter(data_by_week,
                                   x_min=parameters['x_min'],
                                   x_max=parameters['x_max'],
                                   y_min=parameters['y_min'],
                                   y_max=parameters['y_max'])
            print(data_filtered)
            break
        break
    # sql.write(table='seismicity', data=data_filtered, logging_message='earthquakes')


if __name__ == '__main__':
    fire.Fire(collect)