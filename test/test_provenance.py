import os
import pytest
from shutil import rmtree
from tempfile import mkdtemp

from retriever.engines import engine_list
from retriever.lib.defaults import ENCODING, RETRIEVER_REPOSITORY
from retriever.lib.engine_tools import getmd5
from retriever.lib.load_json import read_json
from retriever import commit, install_sqlite

file_location = os.path.normpath(os.path.dirname(os.path.realpath(__file__)))
mysql_engine, postgres_engine, sqlite_engine, msaccess_engine, \
csv_engine, download_engine, json_engine, xml_engine = engine_list

test_commit_details = [
    (
        "dataset_provenance",
        {
            "main": RETRIEVER_REPOSITORY
            + "test/raw_data/dataset-provenance/modified/dataset_provenance.csv"
        },
        {
            "original": "dataset-provenance-c147c9.zip",
            "modified": "dataset-provenance-6ca7c9.zip",
        },
    )
]

test_commit_installation_details = [
    ("dataset-provenance-b8b17d.zip", "aaa2b66a3a77efe416e3555c444f4e2e")
]


def get_script_module(script_name):
    """Load a script module."""
    return read_json(os.path.join(file_location, script_name))


def install_and_commit(script_module, test_dir, commit_message, modified_table_urls=None):
    if modified_table_urls:
        for table in modified_table_urls:
            # modify the url to the csv file
            setattr(script_module.tables[table], "url", modified_table_urls[table])
    sqlite_engine.opts = {
        "install": "sqlite",
        "file": "test_db.sqlite3",
        "table_name": "{db}_{table}",
        "data_dir": ".",
    }
    sqlite_engine.use_cache = False
    # check if dataset is installing properly
    script_module.download(engine=sqlite_engine)
    script_module.engine.final_cleanup()
    commit(script_module, path=test_dir, commit_message=commit_message)


@pytest.mark.parametrize(
    "script_file_name, modified_table_urls, expected_archives", test_commit_details
)
def test_commit(script_file_name, modified_table_urls, expected_archives):
    test_dir = mkdtemp(dir=file_location)
    os.chdir(test_dir)
    script_path = os.path.join(file_location, "raw_data/scripts/", script_file_name)
    script_module = get_script_module(script_path)
    script_json = "{}.json".format(script_path)
    setattr(script_module, "_file", script_json)
    setattr(script_module, "_name", script_file_name.replace("_", "-"))
    # install original version
    install_and_commit(script_module, test_dir=test_dir, commit_message="Original")
    # install modified version
    install_and_commit(
        script_module,
        test_dir=test_dir,
        commit_message="Modified",
        modified_table_urls=modified_table_urls,
    )
    # check if the required archive files exist
    original_archive_path = os.path.join(test_dir, expected_archives["original"])
    original_archive_exist = os.path.isfile(original_archive_path)
    modified_archive_path = os.path.join(test_dir, expected_archives["modified"])
    modified_archive_exist = os.path.isfile(modified_archive_path)
    os.chdir(file_location)
    rmtree(test_dir)

    assert original_archive_exist == True
    assert modified_archive_exist == True


@pytest.mark.parametrize("zip_file_name, expected_md5", test_commit_installation_details)
def test_commit_installation(zip_file_name, expected_md5):
    """Installs the committed dataset in zip to sqlite and then converts
    it to csv to calculate md5 to compare it with the expected_md5"""
    db_name = 'test_sqlite.db'
    zip_file_path = os.path.join(file_location, "raw_data/dataset-provenance/", zip_file_name)
    engine = install_sqlite(zip_file_path, file=db_name, force=True)
    workdir = mkdtemp(dir=file_location)
    os.chdir(workdir)
    engine.to_csv()
    os.chdir(file_location)
    if os.path.isfile(db_name):
        os.remove(db_name)
    calculated_md5 = getmd5(workdir, data_type='dir', encoding=ENCODING)
    rmtree(workdir)
    assert calculated_md5 == expected_md5
