#! /usr/bin/env python
import collections
import os
import json
import io
try:
    from osgeo import ogr
except ImportError:
    pass
from retriever.lib.engine import Engine
from retriever.lib.models import Table
from retriever.lib.datapackage import clean_input
from retriever.lib.tools import open_fw

def get_directory(path):
    return_path = path
    if not os.path.isdir(return_path):
        return_path = os.path.dirname(path)
    return return_path

def create_package(path, datatype, fileFlag, dirFlag, write_out_flag_path, skip_lines):
    path = os.path.expanduser(os.path.normpath(path))
    if not os.path.exists(path):
        print('Please enter a valid path.')

    if write_out_flag_path is not None and write_out_flag_path == '':
        write_out_flag_path = os.path.join(get_directory(path), 'scripts')
    skip_lines = skip_lines[0] if skip_lines else 1

    if datatype.lower() == 'vector':
        create_vector_datapackage(path)
    elif datatype.lower() == 'raster':
        pass
    elif dirFlag:
        process_dirs(path, write_out_flag_path, skip_lines)
    elif fileFlag:
        process_singles(path, write_out_flag_path, skip_lines)


def create_resources(file, skip_lines):
    engine = Engine()
    table = engine.auto_create_table(
        Table(str(file), header_rows=skip_lines), filename=file, make=False)
    cleanTable = table.__dict__
    resourceDict = {}
    pathToTable = os.path.basename(cleanTable['name'])
    resourceDict['name'] = os.path.splitext(pathToTable)[0]
    resourceDict['schema'] = {}
    resourceDict['dialect'] = {}
    resourceDict['schema']['fields'] = []
    for cname, ctuple in cleanTable['columns']:
        resourceDict['schema']['fields'].append(
            {'name': cname, 'type': ctuple[0]})
    resourceDict['url'] = "FILL"
    return resourceDict


def create_script_dict(allpacks, path, file_n, skip_lines):
    allpacks["name"] = "FILL"
    allpacks["title"] = "FILL"
    allpacks["description"] = "FILL"
    allpacks["citation"] = "FILL"
    allpacks["licenses"] = [{"name": "FILL"}]
    allpacks["keywords"] = []
    allpacks["homepage"] = "FILL"
    allpacks["version"] = "1.0.0"
    try:
        resources = create_resources(
            os.path.join(path, file_n), skip_lines)
    except:
        print('Skipped file: ' + file_n)
        return
    allpacks.setdefault('resources', []).append(resources)
    allpacks["retriever"] = "True",
    allpacks["retriever_minimum_version"] = "2.1.0"

    return allpacks


def write_out_scripts(scriptDict, path, write_out_flag_path):
    file_name = os.path.basename(path).split('.')[0] + '.json'
    path_dir = get_directory(os.path.expanduser(path))
    if write_out_flag_path is not None:
        path_dir = os.path.expanduser(write_out_flag_path)
        if not os.path.exists(path_dir):
            os.mkdir(path_dir)
    write_path = os.path.join(path_dir, file_name)

    if not (scriptDict and 'resources' in scriptDict):
        print(write_path + ' creation skipped because resources were empty.')
        return
    if os.path.exists(write_path):
        choice = clean_input(write_path + ' already exists. Overwrite the script? [y/n]')
        if choice == 'n':
            print(write_path + ' creation skipped.')
            return
    try:
        with open_fw(write_path) as outputPath:
            sortedDict = collections.OrderedDict(sorted(scriptDict.items()))
            jsonstr = json.dumps(sortedDict, sort_keys=True, indent=4)
            outputPath.write(jsonstr)
            print('Successfully wrote scripts to ' + os.path.abspath(write_path))
            outputPath.close()
    except Exception as e:
        print(write_path + ' could not be created. {}'.format(e.message))


def process_dirs(sub_dirs_path, write_out_flag_path, skip_lines):
    for path, subdirs, files in os.walk(sub_dirs_path):
        allpacks = collections.OrderedDict()
        for file_n in files:
            if file_n:
                try_create_dict =  create_script_dict(allpacks, path, file_n, skip_lines)
                if try_create_dict:
                    allpacks = try_create_dict
        write_out_scripts(allpacks, path, write_out_flag_path)


def process_singles(single_files_path, write_out_flag_path, skip_lines):
    if os.path.isdir(single_files_path):
        for path, subdirs, files in os.walk(single_files_path):
            for file_n in files:
                allpacks = collections.OrderedDict()
                if file_n:
                    allpacks = create_script_dict(allpacks, path, file_n, skip_lines)
                    filepath = os.path.join(path, file_n)
                    write_out_scripts(allpacks, filepath, write_out_flag_path)
    else:
        directory = os.path.dirname(single_files_path)
        file_name = os.path.basename(single_files_path)
        allpacks = collections.OrderedDict()
        allpacks = create_script_dict(allpacks, directory, file_name, skip_lines)
        write_out_scripts(allpacks, single_files_path, write_out_flag_path)



def get_projection(source, driver_name ='ESRI Shapefile'):
    """Get projection from Layer"""

    data_src = get_source(source, driver_name)
    layer = data_src.GetLayer()
    spatial_ref = layer.GetSpatialRef()
    return spatial_ref.ExportToWkt()

    spatial_ref = layer.GetSpatialRef()
    ref = spatial_ref.ExportToWkt()


def get_source(source, driver_name ='ESRI Shapefile'):
    """Open a data source
    if source is of class osgeo.ogr.DataSource read data source else
    consider it a path and open the path return a data source
    """
    if not isinstance(source, ogr.DataSource):
        try:
            driver = ogr.GetDriverByName(driver_name)
            source = driver.Open(source, 0)
            if source is None:
                print('Could not open %s' % (source))
                exit()

        except:
            raise IOError("Data source cannot be opened")
    return source


def create_vector_datapackage(file_path, driver_name='ESRI Shapefile' ):
    """Create a data package from a vector data source
    the root dir of the vector file becomes the package name
    """
    allpacks = collections.OrderedDict()
    for path, subdirs, files in os.walk(file_path):
        for file_n in files:
            if file_n.endswith(".shp"):
                path_to_dir = os.path.abspath(path)
                dir_name = os.path.basename(path_to_dir)

                file_path_source = os.path.join(path_to_dir, file_n)
                source = os.path.normpath(file_path_source)

                layer_scr = get_source(source, driver_name)
                daLayer = layer_scr.GetLayer()

                allpacks[dir_name] = collections.OrderedDict()
                # spactial ref
                sp_ref = daLayer.GetSpatialRef()
                spatial_ref = "{}".format(str(sp_ref.ExportToWkt()))

                # Json data package dictionary
                allpacks[dir_name]["name"] = daLayer.GetName()
                allpacks[dir_name]["title"] = "The {} dataset".format(daLayer.GetName())
                allpacks[dir_name]["description"] = daLayer.GetDescription()
                allpacks[dir_name]["format"] = "vector" # like  https://specs.frictionlessdata.io/data-resource/ in format: 'csv', 'xls', 'json' here we clasify by type vector or raster
                allpacks[dir_name]["spatial_ref"] = spatial_ref
                allpacks[dir_name]["citation"] = "weaver Pending clarification"
                allpacks[dir_name]["license"] = "Licence for dataset Pending clarification"
                allpacks[dir_name]["driver_name"] ='ESRI Shapefile'
                allpacks[dir_name]["extent"] = OrderedDict(zip(["xMin", "xMax", "yMin", "yMax"], daLayer.GetExtent()))
                allpacks[dir_name]["keywords"] = ["test", "data science", "spatial-data"]
                allpacks[dir_name]["url"] = "FILL"
                allpacks[dir_name]["version"] = "1.0.0"
                allpacks[dir_name]["resources"] = []
                allpacks[dir_name]["retriever"] = "True",
                allpacks[dir_name]["retriever_minimum_version"] = "2.1.0",

                layer = collections.OrderedDict()
                layer["name"] = daLayer.GetName()
                layer["url"] = str(daLayer.GetName())+ "path_to_be_filled"
                layer["geom_type"] = ogr.GeometryTypeToName(daLayer.GetLayerDefn().GetGeomType())
                layer['schema'] = {}
                layer['schema']["fields"] = []
                layerDefinition = daLayer.GetLayerDefn()
                for i in range(layerDefinition.GetFieldCount()):
                    col_obj = collections.OrderedDict()
                    col_obj["name"] = layerDefinition.GetFieldDefn(i).GetName()
                    col_obj["precision"] = layerDefinition.GetFieldDefn(i).GetPrecision()
                    col_obj["type"] = layerDefinition.GetFieldDefn(i).GetTypeName()
                    col_obj["size"] = layerDefinition.GetFieldDefn(i).GetWidth()
                    layer["schema"]["fields"].append(col_obj)
                allpacks[dir_name]["resources"].append(layer)

    for path, subdirs, files in os.walk(file_path):
        for file_n in files:
            if file_n.endswith(".shp"):
                path_to_dir = os.path.abspath(path)
                dir_name = os.path.basename(path_to_dir)
                filenamejson = file_n[:-4].replace("-", "_").replace(".", "") + ".json"
                # file_path_source = os.path.join(r"C:\Users\Henry\Documents\GitHub\Geodata\tutotial_data\Data_2\raster_packages", filenamejson)
                file_path_source = os.path.join('.', filenamejson)
                with open_fw(file_path_source) as output_spec_datapack:
                    json_str = json.dumps(allpacks[dir_name], sort_keys=True, indent=4,
                                          separators=(',', ': '))

                    output_spec_datapack.write(json_str + '\n')

                    output_spec_datapack.close()
