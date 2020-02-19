"""Module to create scripts"""
import collections
import json
import os
from collections import OrderedDict
try:
    from gdalconst import GA_ReadOnly
    from osgeo import gdal
    from osgeo import ogr
    gdal.UseExceptions()
except:
    pass

from retriever.lib.datapackage import clean_input
from retriever.lib.engine import Engine
from retriever.lib.models import Table
from retriever.lib.tools import open_fw


class TabularPk:

    def __init__(self,
                 name="fill",
                 title="fill",
                 description="fill",
                 citation="fill",
                 licenses=[],
                 keywords=[],
                 archived="fill or remove this field if not archived",
                 homepage="fill",
                 version="1.0.0",
                 resources=[],
                 retriever="True",
                 retriever_minimum_version="2.1.0",
                 **kwargs):
        self.name = name
        self.title = title
        self.description = description
        self.citation = citation
        self.licenses = licenses
        self.keywords = keywords
        self.archived = archived
        self.homepage = homepage
        self.version = version
        self.resources = resources
        self.retriever = retriever
        self.retriever_minimum_version = retriever_minimum_version
        for key, item in list(kwargs.items()):
            setattr(self, key, item[0] if isinstance(item, tuple) else item)

    def get_resources(self, file_path, skip_lines=1):
        if isinstance(skip_lines, list):
            skip_lines = skip_lines[0]
        return self.create_tabular_resources(file_path, skip_lines)

    def create_tabular_resources(self, file, skip_lines):
        """Creates resources for the script or errors out if not possible"""
        engine = Engine()
        table_val = Table(str(file), header_rows=skip_lines)
        table = engine.auto_create_table(table_val, filename=file, make=False)
        clean_table = table.__dict__
        resource_dict = {}
        path_to_table = os.path.basename(clean_table["name"])
        print("Processing... {file_name}".format(file_name=path_to_table))
        r_name = os.path.splitext(path_to_table)[0]
        resource_dict["name"] = r_name.replace("_", "-")
        resource_dict["path"] = path_to_table
        resource_dict["schema"] = {}
        resource_dict["dialect"] = {"delimiter": ","}
        resource_dict["schema"]["fields"] = []
        for cname, ctuple in clean_table["columns"]:
            if len(ctuple) >= 2:
                if ctuple[0] == 'char':
                    # char sizes need quotes
                    char_size = "{a}".format(a=ctuple[1])
                    resource_dict["schema"]["fields"].append({
                        "name": cname,
                        "type": ctuple[0],
                        "size": char_size
                    })
                else:
                    resource_dict["schema"]["fields"].append({
                        "name": cname,
                        "type": ctuple[0],
                        "size": ctuple[1]
                    })
            else:
                resource_dict["schema"]["fields"].append({
                    "name": cname,
                    "type": ctuple[0]
                })
        resource_dict["url"] = "fill"
        return resource_dict


class VectorPk(TabularPk):
    pk_formats = ['.shp', "shp"]

    def __init__(self, **kwargs):
        TabularPk.__init__(self, **kwargs)
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.driver_name = 'ESRI Shapefile'
        self.spatial_ref = "spatial_ref"
        self.resources = []

    def get_source(self, source, driver_name='ESRI Shapefile'):
        """Open a data source"""
        driver = ogr.GetDriverByName(driver_name)
        return driver.Open(source, 0)

    def set_globals(self, daLayer):
        self.title = "The {} dataset".format(daLayer.GetName())
        self.description = daLayer.GetDescription()
        self.extent = OrderedDict(
            zip(["xMin", "xMax", "yMin", "yMax"], daLayer.GetExtent()))
        self.geom_type = ogr.GeometryTypeToName(daLayer.GetLayerDefn().GetGeomType())
        sp_ref = daLayer.GetSpatialRef()
        if sp_ref:
            self.spatial_ref = "{}".format(str(sp_ref.ExportToWkt()))

    def create_vector_resources(self, path, file_n, driver_name):
        resource_pk = collections.OrderedDict()
        path_to_dir = get_directory(path)
        dir_name = os.path.basename(path_to_dir)
        file_path_source = path
        source = os.path.normpath(file_path_source)
        layer_scr = self.get_source(source, driver_name)
        daLayer = layer_scr.GetLayer()
        if not self.name:
            self.name = dir_name
        self.set_globals(daLayer)
        resource_pk["resources"] = []
        layer = OrderedDict()
        layer["name"] = daLayer.GetName()
        layer["url"] = str(daLayer.GetName()) + "path_to_be_filled"
        layer["geom_type"] = ogr.GeometryTypeToName(daLayer.GetLayerDefn().GetGeomType())
        layer['schema'] = {}
        layer['schema']["fields"] = []
        layer_definition = daLayer.GetLayerDefn()
        for i in range(layer_definition.GetFieldCount()):
            col_obj = collections.OrderedDict()
            col_obj["name"] = layer_definition.GetFieldDefn(i).GetName()
            col_obj["precision"] = layer_definition.GetFieldDefn(i).GetPrecision()
            col_obj["type"] = layer_definition.GetFieldDefn(i).GetTypeName()
            col_obj["size"] = layer_definition.GetFieldDefn(i).GetWidth()
            layer["schema"]["fields"].append(col_obj)
        return layer

    def get_resources(self, file_path, file_name=None, driver_name=None):
        return self.create_vector_resources(file_path, file_name, self.driver_name)


class RasterPk(TabularPk):
    pk_formats = [
        'gif', 'img', 'bil', 'jpg', 'tif', 'tiff', 'hdf', 'l1b', '.gif', '.img', '.bil',
        '.jpg', '.tif', '.tiff', '.hdf', '.l1b'
    ]
    multi_formats = ["hdf"]

    def __init__(self, **kwargs):
        TabularPk.__init__(self, **kwargs)
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.driver = ""
        self.colums = "src_ds.RasterXSize"
        self.rows = "src_ds RasterYSize"
        self.band_count = "src_ds RasterCount"
        self.datum = "--Coordinate Reference System"
        self.projection = "src_ds GetProjection()"
        self.file_size = "--size of file on disk"
        self.group_count = "--Number of groups in the dataset if applicable"
        self.dataset_count = "--The number of individual datasets"
        self.transform = ""
        self.resources = []

    def get_source(self, mysubdataset_name):
        src_ds = gdal.Open(mysubdataset_name, GA_ReadOnly)
        return src_ds

    def set_global(self, src_ds):
        self.description = os.path.basename(src_ds.GetDescription())
        self.driver = src_ds.GetDriver().ShortName
        self.columns = src_ds.RasterXSize
        self.rows = src_ds.RasterYSize
        self.band_count = src_ds.RasterCount
        self.projection = src_ds.GetProjection()
        self.transform = OrderedDict(
            zip([
                "xOrigin", "pixelWidth", "rotation_2", "yOrigin", "rotation_4",
                "pixelHeight"
            ], src_ds.GetGeoTransform()))

    def create_raster_resources(self, file_path):
        # resource_pk = OrderedDict()
        extension = os.path.splitext(os.path.normpath(file_path))[1]
        fomartx = extension[1:]
        file_name = os.path.basename(file_path)
        base = os.path.splitext(file_name)[0]
        if os.path.isfile(file_path) and fomartx in self.pk_formats:
            # resource_pk["name"] = base
            mysubdataset_name = file_path
            src_ds = self.get_source(mysubdataset_name)
            if not self.name:
                self.name = os.path.basename(src_ds.GetDescription())
            self.set_global(src_ds)

            resource_pk = []
            for band_num in range(1, src_ds.RasterCount + 1):
                bands = OrderedDict()
                srcband = src_ds.GetRasterBand(band_num)
                bands['name'] = base
                bands['path'] = os.path.basename(src_ds.GetDescription())
                bands['band_name'] = base + "_" + str(band_num)
                bands["no_data_value"] = srcband.GetNoDataValue()
                bands["min"] = srcband.GetMinimum()
                bands["max"] = srcband.GetMaximum()
                bands["scale"] = srcband.GetScale()
                bands["color_table"] = None if not srcband.GetRasterColorTable() else True

                bands["statistics"] = OrderedDict(
                    zip(["minimum", "maximum", "mean", "stddev"],
                        srcband.GetStatistics(True, False)))
                resource_pk.append(bands)
        return resource_pk[0]

    def get_resources(self, file_path, skip_lines=None):
        return self.create_raster_resources(file_path)


def create_tabular_datapackage(pk_type, path, file_flag, out_path, skip_lines):
    """Creates tabular package for a path"""
    process_source(pk_type, path, file_flag, out_path, skip_lines)


def create_vector_datapackage(pk_type, path, file_flag, out_path):
    """Creates vector package for a path"""
    process_source(pk_type, path, file_flag, out_path)


def create_raster_datapackage(pk_type, path, file_flag, out_path):
    """Creates raster package for a path"""
    process_source(pk_type, path, file_flag, out_path)


def process_source(pk_type, path, file_flag, out_path, skip_lines=None):
    if file_flag:
        process_singles(pk_type, path, out_path, skip_lines)
    else:
        process_dirs(pk_type, path, out_path, skip_lines)


def get_directory(path):
    """Returns absolute directory path for a path."""
    path = os.path.expanduser(path)
    path = os.path.normpath(path)
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        path = os.path.dirname(path)
    return path


def create_package(path, data_type, file_flag, out_path=None, skip_lines=None):
    """Creates package for a path

    path: string path to files to be processed
    data_type: string data type of the files to be processed
    file_flag: boolean for whether the files are processed as files or directories
    out_path: string path to write scripts out to
    skip_lines: int number of lines to skip as a list []
    """
    path = os.path.expanduser(os.path.normpath(path))
    skip_lines = skip_lines[0] if skip_lines else 1
    if not os.path.exists(path):
        print("Please enter a valid path.")
        return
    if not out_path or out_path == "":
        out_path = os.path.join(get_directory(path), "")
    if data_type.lower() == "tabular":
        tk = TabularPk()
        create_tabular_datapackage(tk, path, file_flag, out_path, skip_lines)
    if data_type.lower() == "vector":
        tk = VectorPk()
        create_vector_datapackage(tk, path, file_flag, out_path)
    if data_type.lower() == "raster":
        tk = RasterPk()
        create_raster_datapackage(tk, path, file_flag, out_path)


def create_script_dict(pk_type, path, file, skip_lines):
    """Create script dict or skips file if resources cannot be made"""
    dict_values = pk_type.__dict__
    try:
        resources = pk_type.get_resources(path, skip_lines)
    except:
        raise
        print("Skipped file: " + file)
        return None
    dict_values.setdefault("resources", []).append(resources)
    return dict_values


def process_dirs(pk_type, sub_dirs_path, out_path, skip_lines):
    """Creates a script for each directory."""
    for path, _, files in os.walk(sub_dirs_path):
        json_pk = collections.OrderedDict()
        for file_name in files:
            if file_name.endswith(".json") or file_name.endswith(".DS_Store"):
                continue
            extension = file_name[file_name.rfind(".") + 1:]
            if hasattr(pk_type, "pk_formats") and extension not in pk_type.pk_formats:
                continue
            if file_name:
                try_create_dict = create_script_dict(pk_type,
                                                     os.path.join(path, file_name),
                                                     file_name, skip_lines)
                json_pk.update(try_create_dict)
        write_out_scripts(json_pk, path, out_path)


def process_singles(pk_type, single_files_path, out_path, skip_lines):
    """Creates a script for each file

    If the filepath is a file, creates a single script for that file.
    If the filepath is a directory, creates a single script for each file in the
    directory.
    """
    if single_files_path.startswith("."):
        return

    if os.path.isdir(single_files_path):
        for path, _, files in os.walk(single_files_path):
            for file_name in files:
                if file_name.endswith(".json") or file_name.endswith(".DS_Store"):
                    continue
                json_pk = collections.OrderedDict()
                if file_name:
                    extension = file_name[file_name.rfind(".") + 1:]
                    if hasattr(pk_type,
                               "pk_formats") and extension not in pk_type.pk_formats:
                        continue
                    filepath = os.path.join(path, file_name)
                    json_pk = create_script_dict(pk_type, filepath, file_name, skip_lines)
                    write_out_scripts(json_pk, filepath, out_path)
    else:
        file_name = os.path.basename(single_files_path)
        json_pk = create_script_dict(pk_type, single_files_path, file_name, skip_lines)
        write_out_scripts(json_pk, single_files_path, out_path)


def write_out_scripts(script_dict, path, out_path):
    """Writes scripts out to a given path"""
    names = os.path.basename(path)
    # file_name = names[:names.rfind(".")] + ".json"
    file_name = names.lower().replace("-", "_") + ".json"
    path_dir = get_directory(os.path.expanduser(path))

    if out_path is not None:
        path_dir = os.path.expanduser(out_path)
        if not os.path.exists(path_dir):
            os.mkdir(path_dir)

    write_path = os.path.join(path_dir, file_name)

    if not (script_dict and "resources" in script_dict):
        print(write_path + " creation skipped because resources were empty.")
        return
    if os.path.exists(write_path):
        choice = clean_input(write_path + " already exists. Overwrite the script? [y/n]")
        if choice == "n":
            print(write_path + " creation skipped.")
            return
    try:
        with open_fw(write_path) as output_path:
            sourted_dict = collections.OrderedDict(script_dict.items())
            json_str = json.dumps(sourted_dict, sort_keys=True, indent=4)
            output_path.write(json_str)
            print("Successfully wrote scripts to " + os.path.abspath(write_path))
            output_path.close()
    except Exception as e:
        print(write_path + " could not be created. {}".format(e.message))
