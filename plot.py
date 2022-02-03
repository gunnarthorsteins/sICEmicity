"""Plots seismic data on a simple map"""

from _datetime import datetime
import matplotlib.pyplot as plt
import shapefile
import pandas as pd
import os

# def plot_shapefile(filename):
#     with shapefile.Reader(f'{folder_loc}{filename}.shp') as shp:
#         for shape in shp.shapeRecords():
#             x = [i[0] for i in shape.shape.points[:]]
#             y = [i[1] for i in shape.shape.points[:]]
#             plt.plot(x, y, 'k', linewidth=0.5)


# if __name__ == '__main__':
#     shp_props = ['elevation', 'waterways', 'dummy']
#     for prop in shp_props:
#         plot_shapefile(prop)

#     dest_file = 'dummy'
#     df_seismic = pd.read_csv(f'{folder_loc}{dest_file}.txt',
#                              sep=";",
#                              header=None,
#                              names=['dt', 'lat', 'lon', 'z', 'M', 'M_L'])
#     df_seismic['dt'] = df_seismic['dt'].astype('datetime64[ns]')

#     plt.scatter(df_seismic['lon'], df_seismic['lat'], c='r', s=2)
#     plt.grid(which="major")
#     vertices_lat = [63.960501, 63.982733, 63.827459, 63.833279]
#     vertices_lon = [-22.219705, -21.906051, -22.248908, -21.887276]
#     plt.axis([min(vertices_lon),
#               max(vertices_lon),
#               min(vertices_lat),
#               max(vertices_lat)])
#     plt.show()
