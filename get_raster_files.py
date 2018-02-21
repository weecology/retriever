import sys
import glob
import numpy as np
import sqlite3
import csv
import linecache
import pandas as pd
import os.path

# Resolve link : https://gis.stackexchange.com/questions/233654/install-gdal-python-binding-on-mac

'''Add proper path variables as follows'''
sys.path.insert(0,'/Library/Frameworks/GDAL.framework/Versions/2.2/Python/3.6/site-packages')


'''Check if ogr, osr, gdal libraries are imported from osgeo'''

try:
    from osgeo import ogr, osr, gdal
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')


'''Check version of GDAL'''

version_num = int(gdal.VersionInfo('VERSION_NUM'))

if version_num < 1100000:
    sys.exit('ERROR: Python bindings of GDAL 1.10 or later required')

#
# HDF5
#

'''Function to get files ending with .h5'''

def get_hdf_file():

    files_hdf = []
    for file in glob.glob("*.h5"):
        files_hdf.append(file)
    return files_hdf

'''Open HDF files from current working directory'''

def open_hdf_file(file_name):

    data = gdal.Open(file_name)
    sub_datasets = data.GetSubDatasets()

    for sds in sub_datasets:
        print(list(sds)[0])
        dataset = gdal.Open(list(sds)[0])
        geotransform = dataset.GetGeoTransform()

        # Check number of rows and columns in HDF dataset
        band = dataset.GetRasterBand(1)
        print("rows = %d columns = %d" % (band.YSize, band.XSize))

        # Check by printing contents of dataset
        print(dataset.ReadAsArray())

def go_through_hdf_file():

    files_hdf = get_hdf_file()

    for file in files_hdf:
        open_hdf_file(file)

#
# GeoTIFF
#

'''Function to get files ending with .tif'''

def get_tif_file():

    files_tif = []
    for file in glob.glob("*.tif"):
        files_tif.append(file)
    return files_tif

'''Loads raster data from TIF image into database'''

def load_tif_data(file_name):

    os.system("rasterlite_load -d {}.sqlite -T {} -D . -t".format(file_name,file_name))
    os.system("rasterlite_load -d {}.sqlite -T {} -D . -v".format(file_name,file_name))

'''Create database for TIF format'''

def create_tif_db():

    files_tif = get_tif_file()

    for file in files_tif:

        file_name = file.strip(".tif")
        database = ("{}.sqlite".format(file_name))
        conn = sqlite3.connect(database)
        curs = conn.cursor()

        curs.execute("SELECT InitSpatialMetadata()")
        curs.fetchall()

        load_data(file_name)

        curs.execute("SELECT tbl_name FROM sqlite_master WHERE type='table';")
        tables = curs.fetchall()

        os.system("mkdir {}_files".format(file_name))

        create_csv(tables, file_name, curs)

'''Create CSV files from existing datasets'''

def create_csv(tables, file_name, curs):

    for i in tables:
        print('Creating CSV for: ',i[0])
        curs.execute("SELECT * FROM {};".format(i[0]))
        ex = curs.fetchall()
        for row in ex :
            list = []
            for j in row:
                value = str(j)
                list.append(value)
            file_data = open('.{}_files/{}.csv'.format(file_name,i[0]), 'a')
            ex = csv.writer(file_data)
            ex.writerow(list)

#
# ESRI GRID
#

def get_grid_files():

    files_grid = []
    for file in glob.glob("*.asc"):
        files_grid.append(file)
    return files_grid

'''Converting asc files into CSV'''

def install_grid(file_name):

    file_name = file_name.strip('.asc')

    file_type = 'asc'
    convert_to = 'csv'

    '''Will overwrite/update file if it already exists'''

    if(os.path.exists('{}.{}'.format(file_name,convert_to))):
        print('{}.{} already exists. Updating..'.format(file_name,convert_to))
        open('{}.{}'.format(file_name,convert_to), 'w').close()
    else:
        print('Installing {}.{}'.format(file_name,convert_to))


    file = open("{}.{}".format(file_name,convert_to),'a')

    '''Fetching meta-data for file'''

    n_col = linecache.getline('{}.{}'.format(file_name,file_type),1).split(' ')
    n_col = n_col[1]

    n_row = linecache.getline('{}.{}'.format(file_name,file_type),2).split(' ')
    n_row = int(n_row[1])

    xllcenter = linecache.getline('{}.{}'.format(file_name,file_type),3).split(' ')
    xllcenter = xllcenter[1]

    yllcenter = linecache.getline('{}.{}'.format(file_name,file_type),4).split(' ')
    yllcenter = yllcenter[1]

    cellsize = linecache.getline('{}.{}'.format(file_name,file_type),5).split(' ')
    cellsize = cellsize[1]

    NODATA_value = linecache.getline('{}.{}'.format(file_name,file_type),6).split(' ')
    NODATA_value = NODATA_value[1]

    results = []

    print("Inserting data..")

    for i in tqdm(range(7,n_row+7)):

        each_line = linecache.getline('{}.{}'.format(file_name,file_type),i).split(' ')
        results.append(list(map(int, each_line)))

    print("Creating CSV..")

    data_frame = pd.DataFrame(results)
    data_frame.to_csv(file, header=False, index=False)

    location = os.path.abspath('{}.{}'.format(file_name,convert_to))

    print("Successful. PATH: {}\n".format(location))

    file.close()

'''Interative for installing for all .asc files'''

def process_grid():

    files = get_grid_files()
    for file in files:
        install_grid(file)

if __name__=='__main__':

    process_grid()

    # insert for TIFF
