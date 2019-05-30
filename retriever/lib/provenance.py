import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from tempfile import NamedTemporaryFile
from zipfile import ZipFile

from retriever import datasets
from retriever.engines import choose_engine
from retriever.lib.defaults import HOME_DIR, VERSION, ENCODING
from retriever.lib.engine_tools import getmd5


def package_details():
    details = {'retriever': VERSION[1:]}
    packages = subprocess.check_output([sys.executable, '-m', 'pip',
                                        'freeze', '--exclude-editable']).decode("utf-8").split('\n')
    for package in packages:
        if package:
            package_name, version = package.split('==')
            details[package_name] = version
    return details


def commit_info(dataset):
    """
    Generate info for a particular commit.
    """
    info = {'packages': package_details(),
            'time': datetime.now(timezone.utc).strftime("%m/%d/%Y, %H:%M:%S"),
            'version': dataset.version}
    return info


def commit(dataset, commit_message='', path='.', quiet=False):
    """
    Commit dataset to a zipped file.
    """
    if type(dataset) == str:
        # if dataset is not a dataset script object find the right script
        dataset = [script for script in datasets() if script.name == dataset][0]
    paths_to_zip = {'script': dataset._file,
                    'raw_data': []}
    raw_dir = os.path.join(HOME_DIR, 'raw_data')
    data_exists = False
    if not quiet:
        print("Committing dataset {}".format(dataset.name))
    try:
        if dataset.name not in os.listdir(raw_dir):
            engine = choose_engine({'command': 'download', 'path': './', 'sub_dir': ""})
            dataset.download(engine=engine, debug=quiet)
            data_exists = True

        elif dataset.name in os.listdir(raw_dir):
            data_exists = True

        if data_exists:
            for root, _, files in os.walk(os.path.join(raw_dir, dataset.name)):
                for file in files:
                    paths_to_zip['raw_data'].append(os.path.join(root, file))

            info = commit_info(dataset)
            info['commit_message'] = commit_message
            info['script_name'] = os.path.basename(dataset._file)

            if os.path.exists(os.path.join(HOME_DIR, 'raw_data', dataset.name)):
                info['md5_dataset'] = getmd5(os.path.join(HOME_DIR, 'raw_data', dataset.name), 'dir', encoding=ENCODING)
            info['md5_script'] = getmd5(dataset._file)
            with ZipFile(os.path.join(path, '{}-{}{}.zip'.format(dataset.name,
                                                                 info['md5_dataset'][:3],
                                                                 info['md5_script'][:3])), 'w') as zipped:
                zipped.write(paths_to_zip['script'],
                             os.path.join('script', os.path.basename(paths_to_zip['script'])))

                for data_file in paths_to_zip['raw_data']:
                    zipped.write(data_file, data_file.replace(raw_dir, ""))

                metadata_temp_file = NamedTemporaryFile()
                with open(os.path.abspath(metadata_temp_file.name), 'w') as json_file:
                    json.dump(info, json_file, sort_keys=True, indent=4)
                zipped.write(os.path.abspath(metadata_temp_file.name), 'metadata.json')
                metadata_temp_file.close()
        if not quiet:
            print("Successfully committed.")
    except Exception as e:
        print("Dataset could not be committed.")
        raise (e)


if __name__ == '__main__':
    for dataset in datasets():
        if dataset.name == 'aquatic-animal-excretion':
            commit(dataset, commit_message='Checking commit', path='/home/apoorva/Desktop/')
