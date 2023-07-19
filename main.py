# Note: I'm letting it fail on the current year if the week
# doesn't exist yet

from fire import Fire
import json
import logging

from sicemicity import scrape, utils

logging.basicConfig(
    filename='logs.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s'
)

with open("config.json") as f:
    config = json.load(f)

defaults = config["default_values"]


def main(**custom_params):
    """Collects seismic data from Icelandic MET by year and week.

    Usage:
        See google-fire docs.
    
    Example:
        $ python3 collect.py --year_min=2000 --year_max=2003
    """

    for parameter, value in custom_params.items():
        defaults[parameter] = value

    years = utils.create_range(defaults['year_min'], defaults['year_max'])
    weeks = utils.create_range(defaults['week_min'], defaults['week_max'])

    for year in years:
        for week in weeks:
            scrape.scrape(year, week)


if __name__ == '__main__':
    Fire(main)