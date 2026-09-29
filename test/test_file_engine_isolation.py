"""File exports must only finalize files owned by their engine instance."""
import csv
import json
import xml.etree.ElementTree as ET

import pytest

from retriever.engines.csvengine import engine as CSVEngine
from retriever.engines.jsonengine import engine as JSONEngine
from retriever.engines.xmlengine import engine as XMLEngine
from retriever.lib.table import TabularDataset
from retriever.lib.templates import BasicTextTemplate


def create_export(engine_class, directory, name):
    engine = engine_class()
    engine.opts = {'data_dir': str(directory), 'table_name': '{table}'}
    engine.table = TabularDataset(name=name, columns=[('value', ('int',))])
    engine.script = BasicTextTemplate(name=name, tables={name: engine.table})
    engine.script_table_registry = {}
    engine.encoding = 'utf-8'
    engine.create_table()
    engine.execute(engine.insert_statement([[1]]))
    return engine


def read_export(engine_class, path):
    if engine_class is JSONEngine:
        return [row['value'] for row in json.loads(path.read_text())]
    if engine_class is XMLEngine:
        return [int(value.text) for value in ET.parse(path).findall('.//value')]
    with path.open(newline='') as stream:
        return [int(row['value']) for row in csv.DictReader(stream)]


@pytest.mark.parametrize('engine_class', [CSVEngine, JSONEngine, XMLEngine])
def test_sequential_exports_preserve_previous_files(engine_class, tmp_path):
    first = create_export(engine_class, tmp_path, 'first')
    first.disconnect()
    original = (tmp_path / 'first').read_bytes()
    second = create_export(engine_class, tmp_path, 'second')
    second.disconnect()

    assert (tmp_path / 'first').read_bytes() == original
    assert read_export(engine_class, tmp_path / 'first') == [1]
    assert read_export(engine_class, tmp_path / 'second') == [1]


@pytest.mark.parametrize('engine_class', [CSVEngine, JSONEngine, XMLEngine])
def test_disconnect_leaves_other_export_writable(engine_class, tmp_path):
    first = create_export(engine_class, tmp_path, 'first')
    second = create_export(engine_class, tmp_path, 'second')
    try:
        first.disconnect()
        second.execute(second.insert_statement([[2]]))
    finally:
        second.disconnect()

    assert read_export(engine_class, tmp_path / 'first') == [1]
    assert read_export(engine_class, tmp_path / 'second') == [1, 2]


@pytest.mark.parametrize('engine_class', [CSVEngine, JSONEngine, XMLEngine])
def test_disconnect_finalizes_all_tables_of_one_export(engine_class, tmp_path):
    engine = create_export(engine_class, tmp_path, 'first')
    engine.table = TabularDataset(name='second', columns=[('value', ('int',))])
    engine.create_table()
    engine.execute(engine.insert_statement([[2]]))
    engine.disconnect()
    engine.disconnect()

    assert read_export(engine_class, tmp_path / 'first') == [1]
    assert read_export(engine_class, tmp_path / 'second') == [2]
