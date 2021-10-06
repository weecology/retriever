"""retriever.lib contains the core Data Retriever modules."""

from .create_scripts import create_package
from .datasets import datasets
from .datasets import dataset_names
from .download import download
from .install import install_csv
from .install import install_json
from .install import install_msaccess
from .install import install_mysql
from .install import install_postgres
from .install import install_sqlite
from .install import install_xml
from .install import install_hdf5
from .provenance import commit, commit_log
from .rdatasets import (update_rdataset_catalog, create_rdataset,
                        update_rdataset_contents, update_rdataset_script,
                        display_all_rdataset_names, get_rdataset_names)
from .repository import check_for_updates
from .engine_tools import reset_retriever
from .fetch import fetch
from .scripts import reload_scripts
from .scripts import get_script_upstream
from .scripts import get_dataset_names_upstream
from .scripts import get_retriever_citation
from .scripts import get_script_citation
from .._version import __version__
from .socrata import (socrata_autocomplete_search, socrata_dataset_info,
                      find_socrata_dataset_by_id, create_socrata_dataset,
                      update_socrata_contents, update_socrata_script)

__all__ = [
    'check_for_updates', 'commit', 'commit_log', 'create_package', 'datasets',
    'dataset_names', 'download', 'reload_scripts', 'reset_retriever', 'install_csv',
    'install_mysql', 'install_postgres', 'install_sqlite', 'install_msaccess',
    'install_json', 'install_xml', 'install_hdf5', 'fetch', 'get_script_upstream',
    'get_dataset_names_upstream', 'get_retriever_citation', 'get_script_citation',
    "__version__", 'socrata_autocomplete_search', 'socrata_dataset_info',
    'find_socrata_dataset_by_id', 'create_socrata_dataset', 'update_socrata_contents',
    'update_socrata_script', 'update_rdataset_catalog', 'create_rdataset',
    'update_rdataset_contents', 'update_rdataset_script', 'display_all_rdataset_names',
    'get_rdataset_names'
]
