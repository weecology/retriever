from __future__ import division
from __future__ import print_function

from future import standard_library

standard_library.install_aliases()
from builtins import zip
from builtins import str
import json
import sys
import pprint
from collections import OrderedDict
from retriever.lib.templates import TEMPLATES
from retriever.lib.models import myTables

if sys.version_info[0] < 3:
    from codecs import open


def compile_json(json_file, debug=False):
    """
    Function to compile JSON script files to python scripts
    The scripts are created with `retriever new_json <script_name>` using
    command line
    """
    json_object = OrderedDict()
    json_file = str(json_file) + ".json"

    try:
        json_object = json.load(open(json_file, "r"))
    except ValueError:
        pass
    if type(json_object) is dict and "resources" in json_object.keys():
        if "format" not in json_object:
            json_object["format"] = "tabular"

        for resource_item in json_object["resources"]:
            # Check for required resource fields
            spec_list = ["name", "url"]

            rspec = set(spec_list)
            if not rspec.intersection(resource_item.keys()) == rspec:
                raise ValueError("Check either {} fields in  Package {}".format(rspec, json_file))

            for spec in spec_list:
                if not resource_item[spec]:
                    raise ValueError("Check either {} for missing values.\n Package {}".format(rspec, json_file))

        json_object["tables"] = {}
        temp_tables = {}
        table_names = [item["name"] for item in json_object["resources"]]
        temp_tables["tables"] = dict(zip(table_names, json_object["resources"]))

        for table_name, table_spec in temp_tables["tables"].items():
            json_object["tables"][table_name] = myTables[json_object["format"]](**table_spec)
        json_object.pop("resources", None)

        return TEMPLATES["default"](**json_object)
    return None
