import json
import os
import pkg_resources
from collections import OrderedDict
from datetime import datetime, timezone
from tempfile import mkdtemp
from importlib import util
from shutil import rmtree
from zipfile import ZipFile

from retriever.engines import choose_engine
from retriever.lib.datasets import datasets
from retriever.lib.defaults import HOME_DIR, ENCODING
from retriever.lib.engine_tools import getmd5
from retriever.lib.load_json import read_json


def package_details():
    details = {}
    packages = pkg_resources.working_set
    for package in packages:
        package_name, version = str(package).split(" ")
        details[package_name] = version
    return details


def commit_info_for_commit(dataset):
    """
    Generate info for a particular commit.
    """
    info = {
        "packages": package_details(),
        "time": datetime.now(timezone.utc).strftime("%m/%d/%Y, %H:%M:%S"),
        "version": dataset.version,
    }
    return info


def commit(dataset, commit_message='', path='.', quiet=False):
    """
    Commit dataset to a zipped file.
    """
    if isinstance(dataset, str):
        # if dataset is not a dataset script object find the right script
        dataset = [script for script in datasets() if script.name == dataset][0]
    paths_to_zip = {"script": dataset._file, "raw_data": []}
    raw_dir = os.path.join(HOME_DIR, "raw_data")
    data_exists = False
    if not quiet:
        print("Committing dataset {}".format(dataset.name))
    try:
        if dataset.name not in os.listdir(raw_dir):
            engine = choose_engine({"command": "download", "path": "./", "sub_dir": ""})
            dataset.download(engine=engine, debug=quiet)
            data_exists = True

        elif dataset.name in os.listdir(raw_dir):
            data_exists = True

        if data_exists:
            for root, _, files in os.walk(os.path.join(raw_dir, dataset.name)):
                for file in files:
                    paths_to_zip["raw_data"].append(os.path.join(root, file))

            info = commit_info_for_commit(dataset)
            info["commit_message"] = commit_message
            info["script_name"] = os.path.basename(dataset._file)
            path_to_raw_data = os.path.join(HOME_DIR, "raw_data", dataset.name)
            if os.path.exists(path_to_raw_data):
                info["md5_dataset"] = getmd5(path_to_raw_data, "dir", encoding=ENCODING)
            info["md5_script"] = getmd5(
                dataset._file, data_type="file", encoding=ENCODING
            )
            zip_file_name = "{}-{}{}.zip".format(
                dataset.name, info["md5_dataset"][:3], info["md5_script"][:3]
            )

            zip_file_path = os.path.join(path, zip_file_name)
            with ZipFile(zip_file_path, "w") as zipped:
                zipped.write(
                    paths_to_zip["script"],
                    os.path.join("script", os.path.basename(paths_to_zip["script"])),
                )
                for data_file in paths_to_zip["raw_data"]:
                    zipped.write(data_file, data_file.replace(raw_dir, ""))
                with open("metadata.json", "w") as json_file:
                    json.dump(info, json_file, sort_keys=True, indent=4)
                zipped.write(os.path.abspath(json_file.name), "metadata.json")
                os.remove("metadata.json")
        if not quiet:
            print("Successfully committed.")
    except Exception as e:
        print(e)
        print("Dataset could not be committed.")
        return


def get_metadata(path_to_archive):
    "Returns a dictionary after reading metadata.json file of a committed dataset"
    with ZipFile(os.path.normpath(path_to_archive), 'r') as archive:
        try:
            metadata = json.loads(archive.read('metadata.json').decode('utf-8'))
        except Exception as e:
            print(e)
            return
    return metadata


def commit_info_for_installation(metadata_info):
    info = {'commit_message': metadata_info['commit_message'], 'time': metadata_info['time'], 'package_not_found': {},
            'package_changed': {}}
    old_package_details = metadata_info['packages']
    current_package_details = package_details()
    if not metadata_info['packages'] == package_details():
        for package in old_package_details:
            if package not in current_package_details:
                info['package_not_found'] = {package: old_package_details[package]}
            elif old_package_details[package] != current_package_details[package]:
                info['package_changed'] = {package: {'old': old_package_details[package],
                                                     'current': current_package_details[package]}}
    return info


def get_script(path_to_archive):
    """
    Reads script from archive.
    """
    with ZipFile(os.path.normpath(path_to_archive), 'r') as archive:
        try:
            commit_details = get_metadata(path_to_archive)
            workdir = mkdtemp(dir=os.path.dirname(path_to_archive))
            archive.extract('/'.join(('script', commit_details['script_name'])), workdir)
            if commit_details['script_name'].endswith('.json'):
                script_object = read_json(os.path.join(workdir, 'script', commit_details['script_name'].split('.')[0]))
            elif commit_details['script_name'].endswith('.py'):
                spec = util.spec_from_file_location("script_module",
                                                    os.path.join(workdir, 'script', commit_details['script_name']))
                script_module = util.module_from_spec(spec)
                spec.loader.exec_module(script_module)
                script_object = script_module.SCRIPT
            rmtree(workdir)
        except Exception as e:
            print(e)
            return
        return script_object


def install_committed(path_to_archive, engine, force=False, quiet=False):
    with ZipFile(os.path.normpath(path_to_archive), 'r') as archive:
        try:
            workdir = mkdtemp(dir=os.path.dirname(path_to_archive))
            engine.data_path = os.path.join(workdir)
            script_object = get_script(path_to_archive)
            details = commit_info_for_installation(get_metadata(path_to_archive))
            if not quiet:
                print('Commit Message:', details['commit_message'])
                print('Time:', details['time'])
                if details['package_not_found'] or details['package_changed']:
                    print("The following requirements are not met.\n"
                          "The installation may fail or not produce required results.")
                    if details["package_not_found"]:
                        print("The following packages were not found:")
                        for package in details['package_not_found']:
                            print("{}=={}".format(package, details['package_not_found'][package]))
                    if details["package_changed"]:
                        print("The following packages have different versions:")
                        for package in details['package_changed']:
                            print("Required: {0}=={1}  Found: {0}=={2}".format(package,
                                                                               details['package_changed'][package]['old'],
                                                                               details['package_changed'][package][
                                                                                   'current']))
            if not force:
                confirm = input("Please enter either y to continue with installation or n to exit:")
                while not (confirm.lower() in ['y', 'n']):
                    print("Please enter either y or n:")
                    confirm = input()
            else:
                confirm = 'y'
            if confirm.lower() == 'y':
                for filename in archive.namelist():
                    if filename.startswith(script_object.name + '/'):
                        archive.extract(filename, workdir)
                engine.script_table_registry = OrderedDict()
                script_object.download(engine)
        except Exception as e:
            print(e)
            return
        finally:
            rmtree(workdir)
        return engine
