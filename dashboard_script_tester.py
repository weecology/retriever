from retriever import install_sqlite
from retriever import datasets
from retriever.engines import engine_list
from status_dashboard import get_dataset_md5, create_diff
import os

mysql_engine, postgres_engine, sqlite_engine, msaccess_engine, csv_engine, download_engine, json_engine, xml_engine = engine_list
file_location = os.path.dirname(os.path.realpath(__file__))
precalculated_md5 = '9f6c106f696451732fb763b3632bfd48'
modified_dataset_url = 'https://raw.githubusercontent.com/apoorvaeternity/sample-dataset/master/modified/Portal_rodents_19772002.csv'


def create_dirs():
    if not os.path.exists(os.path.join(file_location, 'original')):
        os.makedirs(os.path.join(file_location, 'original'))
    if not os.path.exists(os.path.join(file_location, 'modified')):
        os.makedirs(os.path.join(file_location, 'modified'))
    if not os.path.exists(os.path.join(file_location, 'diffs')):
        os.makedirs(os.path.join(file_location, 'diffs'))


def dataset_to_csv(dataset):
    install_sqlite(dataset.name, use_cache=False, file=os.path.join(file_location, 'new_sqlite.db'))
    engine_obj = dataset.checkengine(sqlite_engine)
    engine_obj.to_csv(sort=False)


try:
    create_dirs()
    os.chdir(os.path.join(file_location, 'original'))
    # Add sample-dataset json to the scripts folder
    dataset = [dataset for dataset in datasets() if dataset.name == 'sample-dataset'][0]
    dataset_to_csv(dataset)
    os.remove(os.path.join(file_location, 'new_sqlite.db'))
    setattr(dataset.tables['main'], 'url', modified_dataset_url)
    calculated_md5 = get_dataset_md5(dataset)

    if calculated_md5 != precalculated_md5:
        # If md5 of current dataset doesn't match with current md5 we have to find the diff
        os.chdir(os.path.join(file_location, 'modified'))
        dataset_to_csv(dataset)
        create_diff(os.path.join(file_location, 'original', 'sample_dataset_main.csv'),
                    os.path.join(file_location, 'modified', 'sample_dataset_main.csv'),
                    os.path.join(file_location, 'diffs', 'sample_dataset_main.html'),
                    context=True,numlines=1)
        os.remove(os.path.join(file_location, 'new_sqlite.db'))
except Exception as e:
    print("Error", e)
