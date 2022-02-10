import json
import logging

import pandas as pd
import sqlalchemy

logging.basicConfig(filename=f'logs.log',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')

with open('sql_config.json') as f:
    settings = json.load(f)

dialect = settings['dialect']
engine = settings['engine']
user = settings['user']
password = settings['password']
server = settings['server']
database = settings['database']


def to_sql(df: pd.DataFrame, table_name: str):
    """Writes dataframes to sql database

    Args:
        df (pd.DataFrame): dataframe to be written to database.
            Note that it must have the _exact_ format of the
            database table
        table_name (str): the database table name
    """

    sqlEngine = sqlalchemy.create_engine(
        f'{dialect}+{engine}://{user}:{password}@{server}/{database}',
        pool_pre_ping=True)
    dbConnection = sqlEngine.connect()
    try:
        df.to_sql(table_name, dbConnection, if_exists='append')
        logging.info('Inserted to database')
    except sqlalchemy.exc.IntegrityError:
        logging.warning(
            'SQL insertion error, possibly due to duplicate values')
    except sqlalchemy.exc.OperationalError:
        logging.warning('SQL insertion error, possibly due to \
            incorrectly formatted datetime value')
