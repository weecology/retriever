from retriever import install_sqlite
from retriever import datasets
from retriever.engines import engine_list
from status_dashboard import get_dataset_md5, create_diff
from retriever.lib.defaults import HOME_DIR
import os
import json

mysql_engine, postgres_engine, sqlite_engine, msaccess_engine, csv_engine, download_engine, json_engine, xml_engine = engine_list

file_location = os.path.dirname(os.path.realpath(__file__))
dataset_json_dict = {'encoding': 'ISO-8859-1', 'description': 'Sample dataset for Status Server and Dashboard script.',
                     'retriever_minimum_version': '2.0.dev', 'version': '1.0.0', 'name': 'sample-dataset',
                     'homepage': 'https://support.spatialkey.com/spatialkey-sample-csv-data/', 'retriever': 'True',
                     'title': 'Sample Dataset', 'keywords': ['sample', 'sample-dataset'],
                     'resources': [{
                         'url': 'https://raw.githubusercontent.com/apoorvaeternity/sample-dataset/master/original/FL_insurance_sample.csv',
                         'dialect': {},
                         'name': 'FL_insurance_sample',
                         'schema': {
                             'fields': [
                                 {
                                     'type': 'int',
                                     'name': 'policyID'},
                                 {
                                     'type': 'char',
                                     'name': 'statecode'},
                                 {
                                     'type': 'char',
                                     'name': 'county'},
                                 {
                                     'type': 'float',
                                     'name': 'eq_site_limit'},
                                 {
                                     'type': 'float',
                                     'name': 'hu_site_limit'},
                                 {
                                     'type': 'float',
                                     'name': 'fl_site_limit'},
                                 {
                                     'type': 'float',
                                     'name': 'fr_site_limit'},
                                 {
                                     'type': 'float',
                                     'name': 'tiv_2011'},
                                 {
                                     'type': 'float',
                                     'name': 'tiv_2012'},
                                 {
                                     'type': 'float',
                                     'name': 'eq_site_deductible'},
                                 {
                                     'type': 'float',
                                     'name': 'hu_site_deductible'},
                                 {
                                     'type': 'float',
                                     'name': 'fl_site_deductible'},
                                 {
                                     'type': 'float',
                                     'name': 'fr_site_deductible'},
                                 {
                                     'type': 'float',
                                     'name': 'point_latitude'},
                                 {
                                     'type': 'float',
                                     'name': 'point_longitude'},
                                 {
                                     'type': 'char',
                                     'name': 'line'},
                                 {
                                     'type': 'char',
                                     'name': 'construction'},
                                 {
                                     'type': 'int',
                                     'name': 'point_granularity'}]}}],
                     'citation': 'https://support.spatialkey.com/spatialkey-sample-csv-data/'}

precalculated_md5 = '6ee4a2595fd50e4f4b927ac63a01e6c5'
modified_dataset_url = 'https://raw.githubusercontent.com/apoorvaeternity/sample-dataset/master/modified/FL_insurance_sample.csv'


try:
    if not os.path.exists(os.path.join(file_location, 'original')):
        os.makedirs(os.path.join(file_location, 'original'))
    os.chdir(os.path.join(file_location, 'original'))

    # Add sample-dataset json to the scripts folder
    with open(os.path.join(HOME_DIR, 'scripts', 'sample_dataset.json'), "w") as file:
        json.dump(dataset_json_dict, file)
    dataset = [dataset for dataset in datasets() if dataset.name == 'sample-dataset'][0]
    install_sqlite(dataset.name, use_cache=False, file=os.path.join(file_location, 'new_sqlite.db'))
    engine_obj = dataset.checkengine(sqlite_engine)
    engine_obj.to_csv()
    os.remove(os.path.join(file_location, 'new_sqlite.db'))

    if not os.path.exists(os.path.join(file_location, 'modified')):
        os.makedirs(os.path.join(file_location, 'modified'))

    with open(os.path.join(HOME_DIR, 'scripts', 'sample_dataset.json'), "w") as file:
        dataset_json_dict['resources'][0]['url'] = modified_dataset_url
        json.dump(dataset_json_dict, file)

    if get_dataset_md5(dataset) != precalculated_md5:
        # If md5 of current dataset doesn't match with current md5 we have to find the diff
        os.chdir(os.path.join(file_location, 'modified'))
        install_sqlite(dataset.name, use_cache=False, file=os.path.join(file_location, 'new_sqlite.db'))
        engine_obj = dataset.checkengine(sqlite_engine)
        engine_obj.to_csv()
        if not os.path.exists(os.path.join(file_location, 'diffs')):
            os.makedirs(os.path.join(file_location, 'diffs'))
        create_diff(os.path.join(file_location, 'original', 'sample_dataset_FL_insurance_sample.csv'),
                    os.path.join(file_location, 'modified', 'sample_dataset_FL_insurance_sample.csv'),
                    os.path.join(file_location, 'diffs', 'sample_dataset_FL_insurance_sample_diff.html'))
        os.remove(os.path.join(file_location, 'new_sqlite.db'))
    os.remove(os.path.join(HOME_DIR, 'scripts', 'sample_dataset.json'))
except Exception as e:
    print("Error", e)
