# sICEmicity

Processes seismicity data from The Icelandic MET for analytics.

### Background

The Icelandic Meteorological Office has a rudimentary API. There, all seismic events recorded on its network are dumped, binned by week and year number. The dataset goes all the way back to 1995.

This repo contains everything needed to "data engineer" the dataset, including scraping, parsing, cleaning, filtering, convert coordinates, and saving to a SQL database. That is, the back-end stuff.

### Example Usage

Query parameters can either be hashed in `config.json` or written cli-style as such

`$ python main.py --year_min=1998 --year_max=2006 --x_min=-22.5 --x_max=-22.0`

