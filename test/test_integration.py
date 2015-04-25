"""Integrations tests for EcoData Retriever"""

import os
import shutil
from retriever import HOME_DIR

simple_csv = {'name': 'simple_csv',
              'raw_data': "a,b,c\n1,2,3\n4,5,6",
              'script': "shortname: simple_csv\ntable: simple_csv, http://example.com/simple_csv.txt",
              'expect_out': "a,b,c\n1,2,3\n4,5,6"}

crosstab = {'name': 'crosstab',
            'raw_data': "a,b,c1,c2\n1,1,1.1,1.2\n1,2,2.1,2.2",
            'script': "shortname: crosstab\ntable: crosstab, http://example.com/crosstab.txt\n*column: a, int\n*column: b, int\n*ct_column: c\n*column: val, ct-double\n*ct_names: c1,c2",
            'expect_out': "a,b,c,val\n1,1,c1,1.1\n1,1,c2,1.2\n1,2,c1,2.1\n1,2,c2,2.2"}

tests = [simple_csv, crosstab]
