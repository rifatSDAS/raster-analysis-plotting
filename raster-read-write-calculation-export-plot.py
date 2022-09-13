#!/usr/bin/env python
# coding: utf-8

# Import all packages and libraries
import os
import rasterio
import rasterio.plot
from rasterio.plot import show
from rasterio import plot as rioplot
import numpy as np
import numpy.ma as ma
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
get_ipython().run_line_magic('matplotlib', 'inline')
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep

### make sure rasterio is installed in the system
### if not, follow the installation from
### https://rasterio.readthedocs.io/en/latest/installation.html
### make sure earthpy is also installed
### if not follow the installation from
### https://earthpy.readthedocs.io/en/latest/get-started.html#install-earthpy
### best option is to use anaconda python distribution


# Step 1
# Read and open raster data file
# Example shows to read, open, analysis, and work multiband .bsq file
# And this example can apply for geotiff file format too, just change the file extesion from .bsq to .tif
# Notes: Both raster files must have similar profile, e.g., coordinate system, no. of rows and columns, extensions. If not, then it must be done before applying this Jupyter script.

# open and read file 1
file1 = 'your/file/location/file1.bsq'

with rasterio.open(file1, 'r') as dst1:
    #print(dst1)
    print(dst1.profile)
    print("No. of band:", dst1.count) # to know number of bands
    ### read all bands as a numpy array list
    data1 = dst1.read() # read all raster bands as data1
    print("Shape:", data1.shape) # to know the shape of the list of 2D numpy arrayes
    # plot band 1 for a quick look
    fig, (ax1) = plt.subplots(1,1, figsize=(12,6))
    show((dst1, 1), ax=ax1, cmap='gray', title='band 1')

# open and read file 2
file2 = 'your/file/location/file2.bsq'

with rasterio.open(file2, 'r') as dst2:
    #print(dst2)
    print(dst2.profile)
    print("No. of band:", dst2.count) # to know number of bands
    ### read all bands as a numpy array list
    data2 = dst2.read() # read all raster bands as data2
    print("Shape:", data2.shape) # to know the shape of the list of 2D numpy arrayes
    # plot band 1 for a quick look
    fig, (ax1) = plt.subplots(1,1, figsize=(12,6))
    show((dst2, 1), ax=ax1, cmap='gray', title='band 1')


# Step 2
# Working with full raster area extension
# As an example lets calculate NDVI for each band from multiband 2D numpy arrays
# An iteration over a list of 2D numpy arrays
# Note: Output will be a list of 2d numpy arrays
def ndvi():
    x = data1
    y = data2
    ndvi = ((x - y) / (x + y))
    return ndvi

np.seterr(invalid='ignore') # to ignor RuntimeWarning: invalid value encountered in true_divide

print(type(ndvi))
print(ndvi().shape)
#print(ndvi())

# As an example lets calculate NDVI for a specific band from individual 2D numpy arrays
# Output will be a 2d numpy array
def ndvi1(): #for ndvi of band 1 of data1 and data2
    x = data1[0,:,:]     #[0,:,:] for band 1, [1,:,:] for band 2, [2,:,:] for band 3 and so on
    y = data2[0,:,:]
    ndvi1 = ((x - y) / (x + y))
    return ndvi1

np.seterr(invalid='ignore') # to ignor RuntimeWarning: invalid value encountered in true_divide

print(type(ndvi1))
print(ndvi1().shape)
#print(ndvi1())

# Notes: why two different function names?, I.e., ndvi() and ndvi1()
# Because then each function can call specifically without any naming conflict


# Step 3
# Calculate variables based on mathematical equations
# lets calculate a new variable from our data files called var1
def var1():
    p = 0.12
    c = 2.23
    x = data1
    y = data2
    var1 = ((1 + (p * c)) + x) / (y + (p + c))
    return var1

np.seterr(invalid='ignore') # to ignor RuntimeWarning: invalid value encountered in true_divide

print(type(var1))
print(var1().shape)
#print(var1())

# lets calculate another new variable from our data files called var2
def var2():
    p = 0.12
    c = 2.23
    x = data1
    y = data2
    var2 = ((1 + (p + c)) + x) / (y + (p * c))
    return var2

np.seterr(invalid='ignore') # to ignor RuntimeWarning: invalid value encountered in true_divide

print(type(var2))
print(var2().shape)
#print(var2())


# Step 4
# Let's use var1 and var2 for calculating a new variable
# lets calculate a new variable from var1 and var1 called var3
def var3():
    var3 = ((var2() - var1()) / var1()) * 100
    return var3

np.seterr(invalid='ignore') # to ignor RuntimeWarning: invalid value encountered in true_divide

print(type(var3))
print(var3().shape)
#print(var3())


# Step 5
# Export calculated multiband or single band raster
# Export calculated multiband raster file

# export as multiband geotiff raster
# geotiff is better than bsq format
# for dealing with raster as 2D numpy array
# but we can also export it as bsq file
# then we just need to change .tif to .bsq
# for the example, its exported as .tif format
# Get metadata from any open raster
with rasterio.open(file1) as src:
    meta = src.profile
meta
# export 2D numpy array as geotiff raster layer stack
with rasterio.open(
    "your/output/location/var1.tif", # export directory and export file name and extension
    'w',
    **meta
) as dst:
    dst.write(var1().astype(rasterio.float32))
# change var1() with your multiband 2d numpy array to export

# Export calculated single band raster file
# export as multiband geotiff raster
# geotiff is better than bsq format
# for dealing with raster as 2D numpy array
# but we can also export it as bsq file
# then we just need to change .tif to .bsq
# for the example, its exported as .tif format
# Get metadata from any open raster
with rasterio.open(file1) as src:
    meta = src.profile
meta
# export 2D numpy array as geotiff raster layer stack
with rasterio.open(
    "your/output/location/ndvi-band1.tif", # export directory and export file name and extension
    'w',
    **meta
) as dst:
    dst.write(ndvi1().astype(rasterio.float32), 1) # this command will export a single raster file
# change ndvi1() with your single 2d numpy array to export
# because of converting .bsq to .tif
# a .hdr file will generate in the file directory
# this header file will contain all the info from src
# but, only band 1 is valid raster data, others just false
# open this .hdr file with any text editor
# and make sure inside .hdr file 'band = 1' and 'band names = {Band 1}',
# band name can be anything, so only keep ther first name of the band
# now save the change and close the .hdr file
# you are all set to go!


### <! THIS SECTION IS ONLY NEEDED FOR WORKING WITH AOI OR ROI !> ###

# Working within ROI or AOI or smaller area of raster
# Clip all rasters with an ROI or AOI shape file
# For example a polygon with ESRI shapefile format used
# Clipping must be done for each file individually

import fiona
import rasterio
import rasterio.mask
# open shapefile
with fiona.open("your/polygon/shapefile/location/ROI.shp", "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]
# open the raster for clipping
with rasterio.open("your/output/location/var1.tif") as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta
# write output file into GeoTiff format
# and save it in any directory rather than in system directory
# based on rasterio and python, geotiff format
# is more convinient than bsq format
out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})
with rasterio.open("your/output/location/var1-ROI.tif", "w", **out_meta) as dest:
    dest.write(out_image)

# Notes: Based on working method follow from Step 2 to Step 5

### <! THIS SECTION IS ONLY NEEDED FOR WORKING WITH AOI OR ROI !> ###


# Step 6
# Plotting multiband 2D numpy arrays for quick visualization

titles = ["var3"]
ep.plot_bands(var3(), cols=6)


# Step 7
# Plotting multiband 2D numpy arrays for paper
# It is good idea to call each band or 2D numpy array
# individually and then plot to maintain highest configuration options

# as an example lets plot first three bands of var3
# now define individual bands or 2D numpy array
# from calculated python function, e.g., var3()
band1 = var3()[0,:,:] #[0,:,:] for band 1
band2 = var3()[1,:,:] #[1,:,:] for band 2
band3 = var3()[2,:,:] #[2,:,:] for band 3

# make a function for exporting individual band
# or 2D numpy array as png format figure
# but we can change format, e.g.,
# jpg by change fig_extension="jpg"
OUT_DIR = "your/output/figure/location" # to a specific directory
# or
#OUT_DIR = "." # to root directory of project or where this jupyter script is placed
IMG_ID = "analysis-3" # this name can be any string you like
IMAGE_PATH = os.path.join(OUT_DIR, "images", IMG_ID)
os.makedirs(IMAGE_PATH, exist_ok=True)

def export_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join(IMAGE_PATH, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)

# now plot all these three bands in a single figure
# fix the plot style as default matplotlib figure style
plt.style.use('default')

# define three subplots for each band
plt.subplot(131) # its place band 1 in 1st row 1st column
plt.imshow(band1, cmap='jet') # plot command for band 1 with color map
cbar = plt.colorbar(shrink=0.7) # color bar size
cbar.set_label('[unit]', fontsize=12) # color bar lable
plt.clim(400, 2000) # color bar limit
plt.title('band 1', loc='center', fontsize=15)


plt.subplot(132) # its place band 2 in 1st row 2nd column
plt.imshow(band2, cmap='jet') # plot command for band 2 with color map
cbar = plt.colorbar(shrink=0.7) # color bar size
cbar.set_label('[unit]', fontsize=12) # color bar lable
plt.clim(400, 2000) # color bar limit
plt.title('band 2', loc='center', fontsize=15) # plot title


plt.subplot(133) # its place band 3 in 1st row 3rd column
plt.imshow(band3, cmap='jet') # plot command for band 3 with color map
cbar = plt.colorbar(shrink=0.7) # color bar size
cbar.set_label('[unit]', fontsize=12) # color bar lable
plt.clim(400, 2000) # color bar limit
plt.title('band 3', loc='center', fontsize=15) # plot title

plt.gcf().set_size_inches(18, 6) # fix figure size and fit
export_fig('example-3') # export and save figure by calling python function
