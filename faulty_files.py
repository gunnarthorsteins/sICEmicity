import glob

import collect
import database

files = glob.glob('faulty_files/*')

for file in files:
    data_by_week = collect.scrape(file)
    parsed_data = collect.parse_datetime(data_by_week)
    database.to_sql(df=parsed_data, table_name='seismicity')