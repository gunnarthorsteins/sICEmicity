import json
import logging
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

logging.basicConfig(filename=f'logs.log',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')

with open('sql_config.json') as f:
    settings = json.load(f)

user = settings['user']
password = settings['password']
server = settings['server']
database = settings['database']


def to_sql(df: pd.DataFrame, table_name: str):
    """Writes dataframes to mysql database

    Args:
        df (pd.DataFrame): dataframe to be written to database.
            Note that it must have the exact same format as the
            database table
        table_name (str): the database table name
    """
    sqlEngine = create_engine(
        f'mysql+pymysql://{user}:{password}@{server}/{database}')
    dbConnection = sqlEngine.connect()
    try:
        df.to_sql(table_name, dbConnection, if_exists='append')
        logging.info('Inserted to database')
    except IntegrityError:
        logging.warning(
            'SQL insertion error, possibly due to duplicate values')
