import pandas as pd

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
