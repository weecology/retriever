from retriever import install_sqlite
from retriever import datasets
from retriever.engines import engine_list
from status_dashboard import get_dataset_md5, create_diff
from retriever.lib.defaults import HOME_DIR
import os
import json

mysql_engine, postgres_engine, sqlite_engine, msaccess_engine, csv_engine, download_engine, json_engine, xml_engine = engine_list

file_location = os.path.dirname(os.path.realpath(__file__))
dataset_json_dict = {'keywords': ['mammals', 'desert', 'time-series', 'experimental', 'observational'],
                     'citation': 'S. K. Morgan Ernest, Thomas J. Valone, and James H. Brown. 2009. Long-term monitoring and experimental manipulation of a Chihuahuan Desert ecosystem near Portal, Arizona, USA. Ecology 90:1708.',
                     'scan_lines': '40000',
                     'description': 'The data set represents a Desert ecosystems using the composition and abundances of ants, plants, and rodents has occurred continuously on 24 plots. Currently includes only mammal data.',
                     'retriever_minimum_version': '2.0.dev', 'resources': [
        {
            'url': 'https://raw.githubusercontent.com/apoorvaeternity/sample-dataset/master/original/Portal_rodents_19772002.csv',
            'dialect': {'contains_pk': 'True', 'delimiter': ',', 'missingValues': ['', None]}, 'schema': {
            'fields': [{'type': 'pk-int', 'name': 'recordid'},
                       {'type': 'int', 'name': 'mo'},
                       {'type': 'int', 'name': 'dy'},
                       {'type': 'int', 'name': 'yr'},
                       {'type': 'int', 'name': 'period'},
                       {'type': 'int', 'name': 'plot'},
                       {'type': 'char', 'size': '9', 'name': 'note1'},
                       {'type': 'int', 'name': 'stake'},
                       {'type': 'char', 'size': '9', 'name': 'species'},
                       {'type': 'char', 'size': '9', 'name': 'sex'},
                       {'type': 'char', 'size': '9', 'name': 'age'},
                       {'type': 'char', 'size': '9', 'name': 'reprod'},
                       {'type': 'char', 'size': '9', 'name': 'testes'},
                       {'type': 'char', 'size': '9', 'name': 'vagina'},
                       {'type': 'char', 'size': '9', 'name': 'pregnant'},
                       {'type': 'char', 'size': '9', 'name': 'nipples'},
                       {'type': 'char', 'size': '9', 'name': 'lactation'},
                       {'type': 'int', 'name': 'hfl'},
                       {'type': 'int', 'name': 'wgt'},
                       {'type': 'char', 'size': '9', 'name': 'tag'},
                       {'type': 'char', 'size': '9', 'name': 'note2'},
                       {'type': 'char', 'size': '9', 'name': 'ltag'},
                       {'type': 'char', 'size': '9', 'name': 'note3'},
                       {'type': 'char', 'size': '9', 'name': 'prevrt'},
                       {'type': 'char', 'size': '9', 'name': 'prevlet'},
                       {'type': 'char', 'size': '9', 'name': 'nestdir'},
                       {'type': 'char', 'size': '9', 'name': 'neststk'},
                       {'type': 'char', 'size': '9', 'name': 'note4'},
                       {'type': 'char', 'size': '9', 'name': 'note5'}]},
            'name': 'main'}],
                     'title': 'Portal Project Data (Ernest et al. 2009)',
                     'retriever': 'True',
                     'version': '1.2.1',
                     'homepage': 'https://figshare.com/articles/Data_Paper_Data_Paper/3531317',
                     'name': 'sample-dataset'}

precalculated_md5 = '9f6c106f696451732fb763b3632bfd48'
modified_dataset_url = 'https://raw.githubusercontent.com/apoorvaeternity/sample-dataset/master/modified/Portal_rodents_19772002.csv'

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
    calculated_md5 = get_dataset_md5(dataset)
    if calculated_md5 != precalculated_md5:
        # If md5 of current dataset doesn't match with current md5 we have to find the diff
        os.chdir(os.path.join(file_location, 'modified'))
        install_sqlite(dataset.name, use_cache=False, file=os.path.join(file_location, 'new_sqlite.db'))
        engine_obj = dataset.checkengine(sqlite_engine)
        engine_obj.to_csv()
        if not os.path.exists(os.path.join(file_location, 'diffs')):
            os.makedirs(os.path.join(file_location, 'diffs'))
        create_diff(os.path.join(file_location, 'original', 'sample_dataset_main.csv'),
                    os.path.join(file_location, 'modified', 'sample_dataset_main.csv'),
                    os.path.join(file_location, 'diffs', 'sample_dataset_main.html'))
        os.remove(os.path.join(file_location, 'new_sqlite.db'))
    os.remove(os.path.join(HOME_DIR, 'scripts', 'sample_dataset.json'))
except Exception as e:
    print("Error", e)
