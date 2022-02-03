import fire
import json
import pandas as pd


class Collection:
    def __init__(self):
        with open(f'config.json') as f:
            self.config = json.load(f)

    def get_url(self, year: int, week: int):
        url_raw = self.config['url']
        url = url_raw.replace('YEAR', str(year)).replace('WEEK', str(week))
        return url

    def scrape(self, url: str):
        return pd.read_csv(url, sep=' ', skipinitialspace=True)

def main(year=2021, week=10):

    collection_ = Collection()
    # sql = database.SQL()
    # for year in years:
    #     for week in weeks:
    url = collection_.get_url(year=year, week=week)
    data_by_week = collection_.scrape(url) 
    print(data_by_week)
    # sql.write(table='seismicity', data=tabular_data, logging_mes
    # sage='earthquakes')


if __name__ == '__main__':
    fire.Fire(main)