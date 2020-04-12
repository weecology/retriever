"""Module to auto create scripts from source"""
import collections
import json
import os
from collections import OrderedDict

try:
    from gdalconst import GA_ReadOnly
    from osgeo import gdal
    from osgeo import ogr
    gdal.UseExceptions()
except ImportError as error:
    pass

from retriever.lib.datapackage import clean_input
from retriever.lib.engine import Engine
from retriever.lib.models import Table
from retriever.lib.tools import open_fw


class TabularPk:
    """Main Tabular data package"""

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

    def get_resources(self, file_path, skip_lines=None, encoding="utf-8"):
        """Get resource values from tabular data source"""
        if not skip_lines:
            skip_lines = 1
        return self.create_tabular_resources(file_path, skip_lines, encoding=encoding)

    def create_tabular_resources(self, file, skip_lines, encoding):
        """Create resources for tabular scripts"""
        engine = Engine()
        self.encoding = encoding
        engine.encoding = encoding
        table_val = Table(str(file), header_rows=skip_lines)
        table = engine.auto_create_table(table_val, filename=file, make=False)
        clean_table = table.__dict__
        resource_dict = {}
        path_to_table = os.path.basename(clean_table["name"])
        print("Processing... {file_name}".format(file_name=path_to_table))
        r_name = os.path.splitext(path_to_table)[0].lower()
        resource_dict["name"] = clean_table_name(r_name)
        resource_dict["path"] = path_to_table
        resource_dict["schema"] = {}
        resource_dict["dialect"] = {"delimiter": ","}
        resource_dict["schema"]["fields"] = []
        for cname, ctuple in clean_table["columns"]:
            if len(ctuple) >= 2:
                if ctuple[0] == "char":
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
    """Vector package class"""
    pk_formats = [".shp", "shp"]

    def __init__(self, **kwargs):
        TabularPk.__init__(self, **kwargs)
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.driver_name = "ESRI Shapefile"
        self.spatial_ref = "spatial_ref"
        self.resources = []
        self.extent = ""
        self.geom_type = ""

    def get_source(self, source, driver_name=None):
        """Open a data source"""
        if not driver_name:
            driver_name = self.driver_name
        driver = ogr.GetDriverByName(driver_name)
        return driver.Open(source, 0)

    def set_globals(self, da_layer):
        """Set vector values"""
        self.title = "The {} dataset".format(da_layer.GetName())
        self.description = da_layer.GetDescription()
        self.extent = OrderedDict(
            zip(["xMin", "xMax", "yMin", "yMax"], da_layer.GetExtent()))
        self.geom_type = ogr.GeometryTypeToName(da_layer.GetLayerDefn().GetGeomType())
        sp_ref = da_layer.GetSpatialRef()
        if sp_ref:
            self.spatial_ref = "{}".format(str(sp_ref.ExportToWkt()))

    def create_vector_resources(self, path, driver_name):
        """Create vector data resources"""
        path_to_dir = get_directory(path)
        dir_name = os.path.basename(path_to_dir)
        file_path_source = path
        source = os.path.normpath(file_path_source)
        layer_scr = self.get_source(source, driver_name)
        da_layer = layer_scr.GetLayer()
        if not self.name:
            self.name = dir_name
        self.set_globals(da_layer)
        layer = collections.OrderedDict()
        layer["name"] = clean_table_name(da_layer.GetName())
        layer["url"] = str(da_layer.GetName()) + "path_to_be_filled"
        layer["geom_type"] = ogr.GeometryTypeToName(da_layer.GetLayerDefn().GetGeomType())
        layer["schema"] = {}
        layer["schema"]["fields"] = []
        layer_definition = da_layer.GetLayerDefn()
        for i in range(layer_definition.GetFieldCount()):
            col_obj = collections.OrderedDict()
            col_obj["name"] = layer_definition.GetFieldDefn(i).GetName()
            col_obj["precision"] = layer_definition.GetFieldDefn(i).GetPrecision()
            col_obj["type"] = layer_definition.GetFieldDefn(i).GetTypeName()
            col_obj["size"] = layer_definition.GetFieldDefn(i).GetWidth()
            layer["schema"]["fields"].append(col_obj)
        return layer

    def get_resources(self, file_path, driver_name=None):  # pylint: disable=W0221
        if not driver_name:
            driver_name = self.driver_name
        return self.create_vector_resources(file_path, driver_name)


class RasterPk(TabularPk):
    """Raster package class"""
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
        self.datum = "--Coordinate Reference System"
        self.projection = "src_ds GetProjection()"
        self.file_size = "--size of file on disk"
        self.group_count = "--Number of groups in the dataset if applicable"
        self.dataset_count = "--The number of individual datasets"
        self.transform = ""
        self.resources = []

    def get_source(self, file_path):
        """Read raster data source"""
        if not self.driver:
            # use default open
            src_ds = gdal.Open(file_path, GA_ReadOnly)
        return src_ds

    def set_global(self, src_ds):
        """Set raster specific properties"""
        self.description = os.path.basename(src_ds.GetDescription())
        self.driver = src_ds.GetDriver().ShortName
        self.projection = src_ds.GetProjection()
        self.transform = OrderedDict(
            zip(
                [
                    "xOrigin",
                    "pixelWidth",
                    "rotation_2",
                    "yOrigin",
                    "rotation_4",
                    "pixelHeight",
                ],
                src_ds.GetGeoTransform(),
            ))

    def create_raster_resources(self, file_path):
        """Get resource information from raster file"""
        extension = os.path.splitext(os.path.normpath(file_path))[1]
        fomart_x = extension[1:]
        file_name = os.path.basename(file_path)
        base = os.path.splitext(file_name)[0]
        if os.path.isfile(file_path) and fomart_x in self.pk_formats:
            sub_dataset_name = file_path
            src_ds = self.get_source(sub_dataset_name)
            if not self.name:
                self.name = os.path.basename(src_ds.GetDescription())
            self.set_global(src_ds)

            resource_pk = []
            for band_num in range(1, src_ds.RasterCount + 1):
                bands = OrderedDict()
                srcband = src_ds.GetRasterBand(band_num)
                bands["extensions"] = [fomart_x]
                bands["other_paths"] = ""
                bands["format"] = "raster"
                bands["name"] = clean_table_name(base)
                bands["path"] = os.path.basename(src_ds.GetDescription())
                bands["band_name"] = base + "_" + str(band_num)
                bands["no_data_value"] = srcband.GetNoDataValue()
                bands["scale"] = srcband.GetScale()
                bands["color_table"] = (None
                                        if not srcband.GetRasterColorTable() else True)
                bands["url"] = None
                bands["statistics"] = OrderedDict(
                    zip(
                        ["minimum", "maximum", "mean", "stddev"],
                        srcband.GetStatistics(True, False),
                    ))
                resource_pk.append(bands)
        return resource_pk[0]

    def get_resources(self, file_path):  # pylint: disable=W0221
        """Get raster resources"""
        return self.create_raster_resources(file_path)


def create_tabular_datapackage(pk_type, path, file_flag, out_path, skip_lines, encoding):
    """Creates tabular package for a path"""
    process_source(pk_type, path, file_flag, out_path, skip_lines, encoding)


def create_vector_datapackage(pk_type, path, file_flag, out_path):
    """Creates vector package for a path"""
    process_source(pk_type, path, file_flag, out_path)


def create_raster_datapackage(pk_type, path, file_flag, out_path):
    """Creates raster package for a path"""
    process_source(pk_type, path, file_flag, out_path)


def clean_table_name(table_name):
    """Remove and replace chars `.` and '-' with '_'"""
    path_underscore = table_name.translate(table_name.maketrans("-. ", "___"))
    return "_".join(filter(None, path_underscore.split("_")))


def process_source(pk_type, path, file_flag, out_path, skip_lines=None, encoding="utf-8"):
    """Process source file or source directory"""
    if file_flag:
        process_singles(pk_type, path, out_path, skip_lines, encoding)
    else:
        process_dirs(pk_type, path, out_path, skip_lines, encoding)


def get_directory(path):
    """Returns absolute directory path for a path."""
    path = os.path.expanduser(path)
    path = os.path.normpath(path)
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        path = os.path.dirname(path)
    return path


def create_package(path,
                   data_type,
                   file_flag,
                   out_path=None,
                   skip_lines=None,
                   encoding="utf-8"):
    """Creates package for a path

    path: string path to files to be processed
    data_type: string data type of the files to be processed
    file_flag: boolean for whether the files are processed as files or directories
    out_path: string path to write scripts out to
    skip_lines: int number of lines to skip as a list
    encoding: encoding of source
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
        create_tabular_datapackage(tk, path, file_flag, out_path, skip_lines, encoding)
    if data_type.lower() == "vector":
        tk = VectorPk()
        create_vector_datapackage(tk, path, file_flag, out_path)
    if data_type.lower() == "raster":
        tk = RasterPk()
        create_raster_datapackage(tk, path, file_flag, out_path)


def create_script_dict(pk_type, path, file, skip_lines, encoding):
    """Create a script dict or skips file if resources cannot be made"""
    dict_values = pk_type.__dict__
    try:
        resources = pk_type.get_resources(path, skip_lines, encoding)
    except:
        print("Skipped file: " + file)
        return None
    dict_values.setdefault("resources", []).append(resources)
    return dict_values


def process_dirs(pk_type, sub_dirs_path, out_path, skip_lines, encoding):
    """Creates a script for each directory."""
    json_pk = collections.OrderedDict()
    for path, _, files in os.walk(sub_dirs_path):
        for file_name in files:
            if file_name.endswith(".json") or file_name.endswith(".DS_Store"):
                continue
            extension = file_name[file_name.rfind(".") + 1:]
            if hasattr(pk_type, "pk_formats") and extension not in pk_type.pk_formats:
                continue
            if file_name:
                try_create_dict = create_script_dict(pk_type,
                                                     os.path.join(path, file_name),
                                                     file_name, skip_lines, encoding)
                json_pk.update(try_create_dict)
        write_out_scripts(json_pk, path, out_path)


def process_singles(pk_type, single_files_path, out_path, skip_lines, encoding):
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
                    if (hasattr(pk_type, "pk_formats") and
                            extension not in pk_type.pk_formats):
                        continue
                    filepath = os.path.join(path, file_name)
                    json_pk = create_script_dict(pk_type, filepath, file_name, skip_lines,
                                                 encoding)
                    write_out_scripts(json_pk, filepath, out_path)
    else:
        file_name = os.path.basename(single_files_path)
        json_pk = create_script_dict(pk_type, single_files_path, file_name, skip_lines,
                                     encoding)
        write_out_scripts(json_pk, single_files_path, out_path)


def write_out_scripts(script_dict, path, out_path):
    """Writes scripts out to a given path"""
    names = os.path.basename(path)
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
            sorted_dict = collections.OrderedDict(script_dict.items())
            json_str = json.dumps(sorted_dict, sort_keys=True, indent=4)
            output_path.write(json_str)
            print("Successfully wrote scripts to " + os.path.abspath(write_path))
            output_path.close()
    except Exception as error:
        print(write_path + " could not be created. {}".format(error.message))
