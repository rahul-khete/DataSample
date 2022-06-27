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

import glob
import zipfile
import shutil
import warnings
warnings.filterwarnings("ignore")



import glob
import zipfile
import os
file=glob.glob("*.zip")
with zipfile.ZipFile(file[0], 'r') as zip_ref:
        zip_ref.extractall()
os.remove(file[0])


bands=[]
for root, dirs, files in os.walk("."):
    for f in files:
        s=os.path.relpath(os.path.join(root, f), ".")
        if s.find('R10m')!=-1 or s.find('R20m')!=-1:
            if s.find('B02')!=-1 and s.find('R10m')!=-1:
                bands.append(s)
#                 print(s, ".")
            if s.find('B03')!=-1 and s.find('R10m')!=-1:
                bands.append(s)
#                 print(s, ".")
            if s.find('B04')!=-1 and s.find('R10m')!=-1:
                bands.append(s)
#                 print(s, ".")
            if s.find('B08')!=-1 and s.find('R10m')!=-1:
                bands.append(s)
#                 print(s, ".")
            if s.find('B05')!=-1 and s.find('R20m')!=-1:
               bands.append(s)
#                 print(s, ".")
            if s.find('B11')!=-1 and s.find('R20m')!=-1:
                bands.append(s)



b2 = rio.open(bands[0])
b3 = rio.open(bands[1])
b4 = rio.open(bands[2])
b8 = rio.open(bands[3])
b5 = rio.open(bands[4])
b11 = rio.open(bands[5])


blue=b2.read()
green=b3.read()
red = b4.read()
rededge=b5.read()
nir = b8.read()
swir=b11.read()


upscale_factor = 2
with rio.open(bands[4]) as dataset:

    # resample data to target shape
    rededge = dataset.read(
        out_shape=(
            dataset.count,
            int(dataset.width * upscale_factor),
            int(dataset.height * upscale_factor)
        ),
        resampling=Resampling.bilinear
    )
    
    

upscale_factor = 2
with rio.open(bands[5]) as dataset:

    # resample data to target shape
    swir = dataset.read(
        out_shape=(
            dataset.count,
            int(dataset.width * upscale_factor),
            int(dataset.height * upscale_factor)
        ),
        resampling=Resampling.bilinear
    )


meta = b4.meta
meta.update(driver='GTiff')
meta.update(dtype=rio.float32)

name=bands[0].split('_')[2][4:8]
name=name[2:]+name[:2]
if not os.path.exists('TIF_'+name):
    os.mkdir('TIF_'+name)

path='.\\TIF_'+name+'\\'



def ndviValue(nir,red):
    ndvi = (nir.astype(float)-red.astype(float))/(nir+red)
    with rio.open(path+'NDVI.tif', 'w', **meta) as dst:
        dst.write(ndvi.astype(rio.float32))


    ndvi = rxr.open_rasterio(path+"NDVI.tif",
                                     masked=True).squeeze()

    f, ax = plt.subplots(figsize=(10, 5))
    ndvi.plot.imshow()
    ax.set(title="NDVI")

    ax.set_axis_off()
    plt.show()

    shp = os.path.join('NitrogenFind.shp')

    # Open crop extent (your study area extent boundary)
    crop_extent = geopandas.read_file(shp)
    #crop_extent = crop_extent.set_crs(4326, allow_override=True)
    ndvi_clipped = ndvi.rio.clip(crop_extent.geometry.apply(mapping),
                                          # This is needed if your GDF is in a diff CRS than the raster data
                                          crop_extent.crs)

    f, ax = plt.subplots(figsize=(10, 4))
    ndvi_clipped.plot(ax=ax)
    ax.set(title="Raster Layer Cropped to Geodataframe Extent")
    ax.set_axis_off()
    plt.show()

    pd.DataFrame(ndvi_clipped.values).head()

    ndvi_value=ndvi_clipped.mean()
    return ndvi_value


ndvi_value=ndviValue(nir,red)
print(ndvi_value)


