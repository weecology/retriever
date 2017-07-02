# -*- coding: latin-1  -*-
# """Integrations tests for Data Retriever"""
from __future__ import print_function
import pytest
import subprocess


@pytest.mark.last
def test_compatibility():
    """This tests scripts on 2.0.0 release"""
    output = subprocess.check_output("retriever ls", shell=True)
    assert len(output.split()) == 82
