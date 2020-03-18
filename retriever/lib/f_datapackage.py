import os.path
import yaml
try:
    from datapackage import Package 
except ImportError as e:
    print("Could not import Package - ",e) 
from collections import OrderedDict
from retriever.lib.templates import TEMPLATES
from retriever.lib.models import myTables

from retriever.lib.defaults import SCRIPT_SEARCH_PATHS


"""  Uses url in datapackage.yml to load resources, then downloads the datapackage using datapackage-py
     https://github.com/frictionlessdata/datapackage-py
     cleans the json file with the required changes, then creates script module 
"""

def get_dps():
    """Load the list of data packages from datapackages.yml
    Checks all of the search paths for a datapackages.yml file and loads it into
    a dictionary.
    """
    for path in SCRIPT_SEARCH_PATHS:
        try:
            with open(os.path.join(path, "datapackages.yml"), 'r') as dp_file:
                dp_dict = yaml.safe_load(dp_file)
            return dp_dict
        except:
            pass
    return None

def get_module(dp,url):
    """ Called by scripts.py -> reload_scripts()
        returns script module
    """
    descriptor = get_frictionless(url)
    try: 
        updated_resources = convert_frictionless(descriptor)
    except:
        print("\n problem in converting")
    try:
        module = create_module (descriptor , updated_resources)
    except Exception as e:
        print("\n problems creating mmodule -- ",e)
    return module

def get_frictionless(url):
    """ download frictionless datapackage json file using Package which will return a dict
        Package can handle links to datapackage json file and also links to archive containing the datapackage json.
    """
    try :
        pc = Package(url)
        return pc.descriptor
    except Exception as e:
        print("#Problems downloading the datapackage zip")
        print(e)
        return None
    

def convert_frictionless(descriptor):
    """ Receives datapackage descriptor and does necessary formatting 
        returns only a updated resource dictionary
    """
    type_list = {
        "number" : "double",
        "string" : "string",
        "integer" : "int",
        "boolean" : "string",
        "object" : "string",
        "array" : "string",
        "date" : "string",
        "time" : "string",
        "datetime" : "string",
        "year" : "string",
        "yearmonth" : "string",
        "duration" : "string",
        "geopoint" : "string",
        "geojson" : "string",
        "any" : "string"
    }
    updated_resources = []
    for resource in (descriptor["resources"]):
        if resource["format"]=="csv" and resource["dpp:streamedFrom"].startswith("http"):
            try :
                resource["url"] = resource.pop("dpp:streamedFrom")
                for field in resource["schema"]["fields"]:
                    before_change = field
                    field["name"] = field["name"].strip().replace(" ","_")
                    field["type"] = type_list[field["type"]]
                    resource["schema"]["fields"][resource["schema"]["fields"].index(before_change)] = field
                updated_resources.append(resource)
            except Exception as e:
                updated_resources.append(resource)
                print("exception - ",e)
            
    return updated_resources



def create_module(descriptor , updated_resources):
    """ converts the dict into template class object -- similar to load_json -> read_json()
        returns the object
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
            print("\n inside create module - ",e)  
        descriptor.pop("resources", None)
        return TEMPLATES["default"](**descriptor)    
    return None
