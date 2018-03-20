import glob
import linecache
import pandas as pd
import os
from tqdm import tqdm
import sys

# Resolve link : https://gis.stackexchange.com/questions/233654/install-gdal-python-binding-on-mac

'''Add proper path variables as follows'''
sys.path.insert(0,'/Library/Frameworks/GDAL.framework/Versions/2.2/Python/3.6/site-packages')


'''Check if ogr, osr, gdal libraries are imported from osgeo'''

try:
    from osgeo import ogr, osr, gdal
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')

class Raster:

    raster_extensions = [".asc",".tif"]

    file_grid_locations = []
    file_grid_names = []

    file_tif_locations = []
    file_tif_names = []

    '''Set intial working and target directory'''

    working_directory = os.getcwd() + '/'
    target_directory = working_directory

    '''Calling respective functions to update working and target directory'''

    def __init__(self):

        working_directory = input("Enter FROM Directory [Default => {}]: ".format(self.working_directory))

        if(working_directory==""):
            working_directory = self.working_directory

        target_directory = input("Enter TO Directory [Default => {}]: ".format(self.target_directory))

        if(target_directory==""):
            target_directory = self.target_directory

        self.set_working_directory(working_directory)
        self.set_target_directory(target_directory)


    def set_target_directory(self,target_directory=working_directory):

        try:

            if(os.path.isdir(target_directory)):

                self.target_directory = target_directory

                if(self.target_directory[-1]!='/'):
                    self.target_directory = self.target_directory + '/'

                print('◆ Target Directory: ', self.target_directory)

        except:

            sys.exit("ERROR: No Such Directory")


    def set_working_directory(self,working_directory=working_directory):

        try:

            if(os.path.isdir(working_directory)):

                self.working_directory = working_directory

                if(self.working_directory[-1]!='/'):
                    self.working_directory = self.working_directory + '/'

                print('◆ Working Directory: ', self.working_directory)

        except:

            sys.exit("ERROR: No Such Directory")

    '''Fetch ESRI GRID files from selected working directory'''

    def get_grid_files(self,working_directory=working_directory):

        self.working_directory = working_directory

        for file in glob.glob("{}*.asc".format(working_directory)):

            self.file_grid_locations.append(file)
            self.file_grid_names.append(os.path.basename(file))

        print("❖ ESRI GRID (ASCII) List for PATH={}:".format(working_directory))

        for file in self.file_grid_names:
            print(">>>",file)

        return self.file_grid_locations

    '''Converting asc files into CSV'''

    def install_grid(self,file_path):

        file_name = os.path.basename(file_path)

        file_name = file_name.strip('.asc')

        file_type = 'asc'
        convert_to = 'csv'

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


        os.chdir(self.target_directory)

        '''Will overwrite/update file if it already exists'''

        if(os.path.exists('{}.{}'.format(file_name,convert_to))):
            print('{}.{} already exists. Updating..'.format(file_name,convert_to))
            open('{}.{}'.format(file_name,convert_to), 'w').close()
        else:
            print('Installing {}.{}'.format(file_name,convert_to))


        file = open("{}.{}".format(file_name,convert_to),'a')

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

        os.chdir(self.working_directory)

        file.close()

    '''Interative for installing for all .asc files'''

    def process_grid(self):

        process_iteration = input("◈ Enter file to be processed [Default => all]:")

        if(process_iteration==""):
            process_iteration = "all"

        if(process_iteration=="all"):

            for file in self.file_grid_locations:
                self.install_grid(file)

        else:

            file_name = process_iteration

            file_path = self.working_directory + file_name

            if(file_path in self.file_grid_locations):
                self.install_grid(file_path)
            else:
                print("File Not Found")

    '''Fetch GeoTIFF files from selected working directory'''

    def get_tif_files(self,working_directory=working_directory):

        self.working_directory = working_directory

        for file in glob.glob("{}*.tif".format(working_directory)):

            self.file_tif_locations.append(file)
            self.file_tif_names.append(os.path.basename(file))

        print("GeoTIFF List for PATH={}:".format(working_directory))

        for file in self.file_tif_names:
            print(">>>",file)

    #Create database for TIF format

    def create_tif_db(self):

        for file in self.file_tif_names:

            file_name = file.strip(".tif")

            database = ("{}{}.sqlite".format(target_directory,file_name))
            conn = sqlite3.connect(database)
            curs = conn.cursor()

            curs.execute("SELECT load_extension('mod_rasterlite2')")
            curs.fetchall()

            curs.execute("SELECT load_extension('mod_sqlite')")
            curs.fetchall()

            curs.execute("SELECT InitSpatialMetadataMeta(1)")
            curs.fetchall()

            load_tif_data(self.file_name)

            curs.execute("SELECT tbl_name FROM sqlite_master WHERE type='table';")

            #tables = curs.fetchall()

            #os.system("mkdir {}_files".format(self.file_name))

            #create_csv(tables, self.file_name, curs)

    #Loads raster data from TIF image into database

    def load_tif_data(self,file_name):

        os.system("rasterlite_load -d {}.sqlite -T {} -D . -t".format(file_name,file_name))
        os.system("rasterlite_load -d {}.sqlite -T {} -D . -v".format(file_name,file_name))


if __name__=='__main__':

    r = Raster()
    r.get_tif_files()
    #r.get_grid_files()
