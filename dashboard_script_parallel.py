from multiprocessing import Pool
from retriever import datasets
from retriever import install_sqlite
import time
import os

start_time = time.time()

example_datasets = ['biodiversity-response', 'airports', 'portal', 'bird-size', 'gdp']


def install(dataset):
    print(dataset.name)
    database_name = '{}_sqlite.db'.format(dataset.name.replace('-', '_'))
    install_sqlite(dataset.name, use_cache=False, file=database_name)
    print("Successfully installed==>", dataset.name)
    os.remove(database_name)

if __name__ == '__main__':
    pool = Pool(3)
    pool.map(install, [dataset for dataset in datasets() if dataset.name in example_datasets])
print("Time taken={time_taken} seconds".format(time_taken=time.time() - start_time))
