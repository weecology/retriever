"""downloads the datapackage using datapackage-py
https://github.com/frictionlessdata/datapackage-py
Convert Frictionless specs to Data Retriever specs
"""

import os.path
import yaml

from datapackage import Package
from collections import OrderedDict

from retriever.lib.templates import TEMPLATES
from retriever.lib.models import myTables
from retriever.lib.defaults import SCRIPT_SEARCH_PATHS


def get_dps():
    """Load the first datapackages.yml in the script search path.

    Default dp_dict should be name and empty resources
    """
    dp_dict = OrderedDict()
    for path in SCRIPT_SEARCH_PATHS:
        try:
            if os.path.isfile(os.path.join(path, "datapackages.yml")):
                with open(os.path.join(path, "datapackages.yml"), 'r') as dp_file:
                    dp_dict = yaml.safe_load(dp_file)
                return dp_dict
        except:
            pass
    return dp_dict


def get_module(dp, url, dont_download=True):
    """Return script module"""
    try:
        if dont_download:
            descriptor = {"name": dp, "resources": []}
        else:
            descriptor = get_frictionless(url)
        updated_resources = convert_frictionless(descriptor)
        module = create_module(descriptor, updated_resources)
        return module
    except Exception as e:
        print("There was a problem converting the Frictionless"
              "Data package into Retriever recipe :", dp)
        print(e)
        return None


def get_frictionless(url):
    """Download frictionless datapackage json file using the datapackage library"""
    try:
        pc = Package(url)
        return pc.descriptor
    except Exception as e:
        print("Unable to download file from :", url)
        print(e)
        return None


def convert_frictionless(descriptor):
    """Convert frictionless data package data types to Data Retriever data types."""
    type_list = {
        "number": "double",
        "string": "string",
        "integer": "int",
        "boolean": "string",
        "object": "string",
        "array": "string",
        "date": "string",
        "time": "string",
        "datetime": "string",
        "year": "string",
        "yearmonth": "string",
        "duration": "string",
        "geopoint": "string",
        "geojson": "string",
        "any": "string"
    }
    updated_resources = []
    rec={}
    for resource in (descriptor["resources"]):
        rec["name"] = resource["name"].replace(" ", "_").replace("-", "_")
        if "path" in resource:
            rec["url"] = resource["path"]
        if "dpp:streamedFrom" in resource:
            rec["url"] = resource["dpp:streamedFrom"]
        if "dialect" in resource:
            if "delimiter" in resource["dialect"]:
                rec["dialect"] = {"delimiter" : resource["dialect"]["delimiter"]}

        if "schema" in resource and "fields" in resource["schema"]:
            rec["schema"] = {"fields":[]}
            for field in resource["schema"]["fields"]:
                field["name"] = field["name"].strip().replace(" ", "_")
                field["type"] = type_list[field["type"]]
                rec["schema"]["fields"].append(field)

        updated_resources.append(rec)
    descriptor["resources"] = updated_resources
        # resource["name"] = resource["name"].replace(" ", "_").replace("-", "_")
        # r
        # if resource["format"] == "csv" and resource["dpp:streamedFrom"].startswith(
        #         "http"):
        #
        # if resource["format"] and resource["dpp:streamedFrom"]:
        #     try:
        #         # resource["url"] = resource.pop("dpp:streamedFrom")
        #         resource["name"] = resource["name"].replace(" ", "_").replace("-", "_")
        #         resource["url"] = resource["dpp:streamedFrom"]
        #         for field in resource["schema"]["fields"]:
        #             before_change = field
        #             field["name"] = field["name"].strip().replace(" ", "_")
        #             field["type"] = type_list[field["type"]]
        #             resource["schema"]["fields"][resource["schema"]["fields"].index( before_change)] = field
        #         updated_resources.append(resource)
        #     except Exception as e:
        #         print("Failed to convert Frictionless to Retriever data types ")
        #         print(e)
    return updated_resources


def create_module(descriptor, updated_resources):
    """Converts the dict into template class object

    Similar to load_json after read_json
    returns the script module object
    """
    if isinstance(descriptor, dict) and "resources" in descriptor.keys():
        for resource in updated_resources:
            if "url" in resource:
                if "urls" in descriptor:
                    descriptor["urls"][resource["name"]] = resource["url"]
        descriptor["tables"] = OrderedDict()
        temp_tables = {}
        table_names = [item["name"] for item in updated_resources]
        temp_tables["tables"] = OrderedDict(zip(table_names, updated_resources))
        try:
            for table_name, table_spec in temp_tables["tables"].items():
                table_spec["format"] = "tabular"
                table_spec.pop("path")
                descriptor["tables"][table_name] = myTables["tabular"](**table_spec)
        except Exception as e:
            print(e, "kkkkkk")
        descriptor.pop("resources", None)
        return TEMPLATES["default"](**descriptor)
    return None
