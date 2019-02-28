from __future__ import division
from __future__ import print_function

from future import standard_library

standard_library.install_aliases()
from builtins import zip
from builtins import str
import json
from collections import OrderedDict
from retriever.lib.templates import TEMPLATES
from retriever.lib.models import myTables
from retriever.lib.tools import open_fr


def read_json(json_file, debug=False):
    """Read Json dataset package files

    Load each json and get the appropriate encoding for the dataset
    Reload the json using the encoding to ensure correct character sets
    """
    json_object = OrderedDict()
    json_file_encoding = None
    json_file = str(json_file) + ".json"

    try:
        file_obj = open_fr(json_file)
        json_object = json.load(file_obj)
        if "encoding" in json_object:
            json_file_encoding = json_object['encoding']
        file_obj.close()
    except ValueError:
        pass

    # Reload json using encoding if available
    try:
        if json_file_encoding:
            file_obj = open_fr(json_file, encoding=json_file_encoding)
        else:
            file_obj = open_fr(json_file)
        json_object = json.load(file_obj)
        file_obj.close()

    except ValueError:
        pass
    if type(json_object) is dict and "resources" in json_object.keys():

        # Note::formats described by frictionlessdata data may need to change
        tabular_exts = {"csv", "tab"}
        vector_exts = {"shp", "kmz"}
        raster_exts = {"tif", "tiff", "bil",
                           "hdr", "h5", "hdf5", "hr", "image"}
        for resource_item in json_object["resources"]:
            if "format" not in resource_item:
                if "format" in json_object:
                    resource_item["format"] = json_object["format"]
                else:
                    resource_item["format"] = "tabular"
            if "extensions" in resource_item:
                exts = set(resource_item["extensions"])
                if exts <= tabular_exts:
                    resource_item["format"] = "tabular"
                elif exts <= vector_exts:
                    resource_item["format"] = "vector"
                elif exts <= raster_exts:
                    resource_item["format"] = "raster"
            if "url" in resource_item:
                if "urls" in json_object:
                    json_object["urls"][resource_item["name"]] = resource_item["url"]

        json_object["tables"] = OrderedDict()
        temp_tables = {}
        table_names = [item["name"] for item in json_object["resources"]]
        temp_tables["tables"] = OrderedDict(zip(table_names, json_object["resources"]))
        for table_name, table_spec in temp_tables["tables"].items():
            json_object["tables"][table_name] = myTables[
                temp_tables["tables"][table_name]["format"]
            ](**table_spec)
        json_object.pop("resources", None)
        return TEMPLATES["default"](**json_object)
    return None
