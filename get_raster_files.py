import sys
import glob
import os

'''Add proper path variables as follows'''
sys.path.insert(0,'/Library/Frameworks/GDAL.framework/Versions/2.2/Python/3.6/site-packages')

try:
	from osgeo import gdal
	print("Gdal Version: ",gdal.__version__,"\n")
except:
	sys.exit("Cannot find osgeo")

class raster:

    files = []
    formats = ('*.tif','*.png','*.jpg','*.asc','*.ecw','*.jpeg')

    def __init__(self):

        self.get_files()
        self.load_files()

    def get_files(self):

    	for types in self.formats:
    		self.files.extend(glob.glob(types))
    	for content in self.files:
    		print(content)

    def load_files(self):

        os.system('spatialite RasterDB.sqlite ".databases"')

        for file in self.files:
            base = os.path.basename(file)
            name = os.path.splitext(base)[0]
            ext = os.path.splitext(base)[1]

            if(ext==".tif"):
                os.system("rasterlite_load -d RasterDB.sqlite -T {} -D . -i tiff".format(name))
            if(ext==".jpg"):
                os.system("rasterlite_load -d RasterDB.sqlite -T {} -D . -i jpg".format(name))
            if(ext==".jpeg"):
                os.system("rasterlite_load -d RasterDB.sqlite -T {} -D . -i jpeg".format(name))
            if(ext==".ecw"):
                os.system("rasterlite_load -d RasterDB.sqlite -T {} -D . -i wavelet".format(name))
            if(ext==".png"):
                os.system("rasterlite_load -d RasterDB.sqlite -T {} -D . -i png".format(name))

if __name__ == "__main__":
    obj = raster()
