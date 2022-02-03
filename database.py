import json
import pandas as pd
import pymysql
from sqlalchemy import create_engine

with open('sql_config.json') as f:
    settings = json.load(f)

user = settings['user']
password = settings['password']
server = settings['server']
database = settings['database']

def to_sql(df: pd.DataFrame, table_name: str):
    sqlEngine = create_engine(f'mysql+pymysql://{user}:{password}@{server}/{database}')
    dbConnection = sqlEngine.connect()
    df.to_sql(table_name, dbConnection, if_exists='append')