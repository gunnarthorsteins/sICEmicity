import json
import sqlite3

import pandas as pd


with open('config.json') as f:
    config = json.load(f)


def write(df: pd.DataFrame, table_name: str):
    """Writes dataframes to sql database

    Args:
        df (pd.DataFrame): dataframe to be written to database.
            Note that it must have the _exact_ format of the
            database table
        table_name (str): the database table name
    """

    connection = sqlite3.connect(config['database'])
    df.to_sql(name=table_name, con=connection)