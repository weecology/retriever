import json
import os
from collections import OrderedDict
from datetime import datetime, timezone
from shutil import rmtree
from tempfile import mkdtemp
from zipfile import ZipFile

import pkg_resources

from retriever.engines import choose_engine
from retriever.lib.datasets import datasets
from retriever.lib.defaults import ENCODING, HOME_DIR, PROVENANCE_DIR
from retriever.lib.engine_tools import getmd5
from retriever.lib.provenance_tools import get_metadata, get_script_provenance


def package_details():
    """
    Returns a dictionary with details of installed packages in the current environment
    """
    details = {}
    packages = pkg_resources.working_set
    for package in packages:  # pylint: disable=E1133
        details[package.project_name] = package.version
    return details


def commit_info_for_commit(dataset, commit_message):
    """
    Generate info for a particular commit.
    """
    info = {
        "packages": package_details(),
        "time": datetime.now(timezone.utc).strftime("%m/%d/%Y, %H:%M:%S"),
        "version": dataset.version,
        "commit_message": commit_message,
        "script_name": os.path.basename(dataset._file),
    }
    path_to_raw_data = os.path.join(HOME_DIR, "raw_data", dataset.name)
    if os.path.exists(path_to_raw_data):
        info["md5_dataset"] = getmd5(path_to_raw_data, "dir", encoding=ENCODING)
    info["md5_script"] = getmd5(dataset._file, data_type="file", encoding=ENCODING)
    return info


def commit_writer(dataset, commit_message, path, quiet):
    """Creates the committed zipped file"""

    paths_to_zip = {"script": dataset._file, "raw_data": []}
    raw_dir = os.path.join(HOME_DIR, "raw_data")
    data_exists = False
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

        info = commit_info_for_commit(dataset, commit_message=commit_message)
        zip_file_name = "{}-{}{}.zip".format(dataset.name, info["md5_dataset"][:3],
                                             info["md5_script"][:3])

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


def commit(dataset, commit_message='', path=None, quiet=False):
    """
    Commit dataset to a zipped file.
    """
    if isinstance(dataset, str):
        # if dataset is not a dataset script object find the right script
        dataset_list = [
            script for script in datasets()['offline'] if script.name == dataset
        ]
        dataset = dataset_list[0]
    dataset_provenance_path = (None
                               if path else os.path.join(PROVENANCE_DIR, dataset.name))
    if not path and not os.path.exists(dataset_provenance_path):
        os.makedirs(dataset_provenance_path)
    path = path if path else dataset_provenance_path
    if not quiet:
        print("Committing dataset {}".format(dataset.name))
    try:
        commit_writer(dataset=dataset,
                      commit_message=commit_message,
                      path=path,
                      quiet=quiet)
        if not quiet:
            print("Successfully committed.")
    except Exception as e:
        print(e)
        print("Dataset could not be committed.")
        return


def commit_info_for_installation(metadata_info):
    """
    Returns a dictionary with commit info and changes in old and current environment
    """
    info = {
        'commit_message': metadata_info['commit_message'],
        'time': metadata_info['time'],
        'package_not_found': {},
        'package_changed': {},
    }
    old_package_details = metadata_info['packages']
    current_package_details = package_details()
    if not metadata_info['packages'] == package_details():
        for package in old_package_details:
            if package not in current_package_details:
                info['package_not_found'] = {package: old_package_details[package]}
            elif old_package_details[package] != current_package_details[package]:
                info['package_changed'] = {
                    package: {
                        'old': old_package_details[package],
                        'current': current_package_details[package],
                    }
                }
    return info


def installation_details(metadata_info, quiet):
    """
    Outputs details of the commit for eg. commit message, time, changes in environment
    """
    details = commit_info_for_installation(metadata_info=metadata_info)
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
                    old_version = details['package_changed'][package]['old']
                    current_version = details['package_changed'][package]['current']
                    message = "Required: {0}=={1}  Found: {0}=={2}"
                    print(message.format(package, old_version, current_version))


def install_committed(path_to_archive, engine, force=False, quiet=False):
    """
    Installs the committed dataset
    """
    with ZipFile(os.path.normpath(path_to_archive), 'r') as archive:
        try:
            workdir = mkdtemp(dir=os.path.dirname(path_to_archive))
            engine.data_path = os.path.join(workdir)
            script_object = get_script_provenance(path_to_archive=path_to_archive)
            metadata_info = get_metadata(path_to_archive=path_to_archive)
            installation_details(metadata_info=metadata_info, quiet=quiet)
            if not force:
                confirm = input(
                    "Please enter either y to continue with installation or n to exit:")
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
            return engine
        except Exception as e:
            print(e)
            return None
        finally:
            engine.data_path = None
            rmtree(workdir)


def commit_log(dataset):
    """
    Shows logs for a committed dataset which is in provenance directory
    """
    try:
        committed_dataset_path = os.path.join(PROVENANCE_DIR, dataset)
        if os.path.exists(committed_dataset_path):
            log = {}
            for root, _, files in os.walk(committed_dataset_path):
                zip_files = (file_obj for file_obj in files if file_obj.endswith(".zip"))
                for zip_file in zip_files:
                    archive_path = os.path.join(root, zip_file)
                    commit_info = get_metadata(path_to_archive=archive_path)
                    commit_datetime = datetime.strptime(commit_info['time'],
                                                        "%m/%d/%Y, %H:%M:%S")
                    log[commit_datetime] = (
                        commit_info['commit_message'],
                        '{}{}'.format(
                            commit_info["md5_dataset"][:3],
                            commit_info["md5_script"][:3],
                        ),
                    )
            # sort the commits according to time in reverse order
            # i.e. latest commit is the first element
            sorted_log = sorted(log.items(), reverse=True)
            for commit_value in sorted_log:
                print('\nCommit message:', commit_value[1][0])
                print('Hash:', commit_value[1][1])
                print('Date:', commit_value[0].strftime("%m/%d/%Y, %H:%M:%S"))
            return sorted_log
        print("No logs for {}".format(dataset))
        return None
    except Exception as e:
        print("Unable to generate log for", dataset)
        print(e)
        return None
