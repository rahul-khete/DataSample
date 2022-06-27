import geopandas
from sentinelsat import SentinelAPI
import numpy as np
import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import MultiPolygon, Polygon,mapping
import rasterio as rio
from rasterio.enums import Resampling
from rasterio import plot
from rasterio.plot import show
from zipfile import ZipFile
import matplotlib.pyplot as plt
from osgeo import gdal,osr
import os
import math
import fiona
from branca.element import Figure

import rioxarray as rxr
import xarray as xr
import earthpy as et
import earthpy.plot as ep

import warnings
warnings.filterwarnings("ignore")





nReserve = geopandas.read_file('.\\KolhapurSite\\KolhapurSite.shp')

m2 = folium.Map([16.7593142,77.1740536], zoom_start=12)
folium.GeoJson(nReserve).add_to(m2)
# m2

footprint =None
for i in nReserve['geometry']:
    footprint = i
    

user = 'aniket.mane.1238' 
password = 'Aniket@1238' 
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')


products = api.query(footprint,
                     date = ('20220415', '20220421'),
                     platformname = 'Sentinel-2',
                     processinglevel = 'Level-2A',
                     cloudcoverpercentage = (0,100)
                    )


products_gdf = api.to_geodataframe(products)

api.download(products_gdf['uuid'][0])
