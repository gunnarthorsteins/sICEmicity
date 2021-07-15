"""Filters seismic data by lat and lon and merges into one large file.

Disclaimer: Hadn't learned to use Pandas when writing, so don't judge the utter crudeness.
'If it looks stupid but works then it ain't stupid' - Jamie Hyneman
"""

import csv
import os


my_dir = os.getcwd()
folder_loc = my_dir.rsplit("\\", 1)[0] + "\\1. Data\\1. Earthquakes\\"  # Don't even ask
dest_file = folder_loc


# Dummmy vertices
vertices_lat = [63.960501, 63.982733, 63.827459, 63.833279]
vertices_lon = [-22.219705, -21.906051, -22.248908, -21.887276]

year_start = 1995
year_end = 2021
my_range = 53
try:
    for year in range(year_start, year_end + 1):
        for week in range(1, my_range):
            # Looking at every file
            file_loc = f'{folder_loc}1. Raw/{str(year)}/Earthquakes_{str(year)}_{str(week)}.txt'
            with open(file_loc, mode='r') as raw_data_file:
                line_list = raw_data_file.readlines()
                for i in range(2, len(line_list), 2):
                    line_value = line_list[i]
                    line_value = line_value.split(" ")
                    line_value = list(filter(None, line_value))

                    lat = float(line_value[3])
                    lon = float(line_value[4])
                    if lon > min(vertices_lon) and lon < max(vertices_lon):
                        if lat > min(vertices_lat) and lat < max(vertices_lat):
                            Z = line_value[5]
                            M = line_value[6]
                            Ml = float(line_value[7])

                            date = line_value[1]
                            time = line_value[2]
                            dt = date[:4]+"."+date[4:6]+"."+date[6:]+" " + \
                                 time[0:2]+":"+time[2:4]+":"+time[4:6]

                            with open(dest_file, mode='a') as filt_file:
                                my_writer = csv.writer(filt_file,
                                                       delimiter=";",
                                                       lineterminator="\n")
                                my_writer.writerow([dt, lat, lon, Z, M, Ml])


except Exception as e:
    print(str(e))
    raise SystemExit
