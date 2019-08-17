# -*- coding: UTF-8 -*-
#retriever

import json
import os

import requests

from retriever.lib.templates import Script

try:
    from retriever.lib.defaults import VERSION
except ImportError:
    from retriever import VERSION


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "3D Elevation Program (3DEP) high-quality U.S. " \
                     "Geological Survey topographic data"
        self.name = "usgs-elevation"
        self.retriever_minimum_version = '2.0.dev'
        self.version = '1.0.0'
        self.ref = "https://pubs.er.usgs.gov/publication/fs20163022"
        self.citation = "Lukas, Vicki, Stoker, J.M., 2016, " \
                        "3D Elevation Program—Virtual USA in 3D: U.S. " \
                        "Geological Survey Fact Sheet 2016–3022, 1 p., " \
                        "http://dx.doi.org/10.3133/fs20163022."
        self.description = "The U.S. Geological Survey (USGS) " \
                           "3D Elevation Program (3DEP) " \
                           "uses lidar to create a virtual reality maps."
        self.keywords = ["Elevation", "Map", "lidar", "Radar"]

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        # IMG
        request_query = "https://viewer.nationalmap.gov/tnmaccess/api/products?&bbox={}&q=&start=&end=&dateType=&datasets=National+Elevation+Dataset+(NED)+1/3+arc-second&prodFormats=IMG&prodExtents=1+x+1+degree&polyCode=&polyType=&max=40&offset=0&_=1519665242114".format(",".join(str(i) for i in engine.opts["bbox"] if i))
        engine = self.engine
        res = requests.get(request_query).text
        data_url = json.loads(res)

        from retriever.lib.table import RasterDataset
        for item in data_url["items"]:
            engine.download_files_from_archive(item["downloadURL"])
        for raster_files in engine.supported_raster(engine.format_data_dir(),
                                                    [".img"]):
            base_name = os.path.basename(raster_files)
            filename, file_extension = os.path.splitext(base_name)
            table = RasterDataset(name=filename)
            engine.table = table
            engine.auto_create_table(table,
                                     filename=os.path.basename(raster_files))
            engine.insert_raster(raster_files)

SCRIPT = main()
