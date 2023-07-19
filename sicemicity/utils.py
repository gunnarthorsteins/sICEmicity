import numpy as np
import pandas as pd


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



def create_range(min_, max_):
    # +1 b/c of Python's zero-based index
    return np.arange(min_, max_ + 1)