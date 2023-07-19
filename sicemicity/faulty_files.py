import glob

import main
import sicemicity.database as database

files = glob.glob('faulty_files/*')

for file in files:
    data_by_week = main.scrape(file)
    parsed_data = main.parse_datetime(data_by_week)
    database.write(df=parsed_data, table_name='seismicity')