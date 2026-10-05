"""Exporting installed JSON/XML data must leave it available for reuse."""
import csv
import json
from types import SimpleNamespace

import pytest

from retriever.engines.jsonengine import engine as JSONEngine
from retriever.engines.xmlengine import engine as XMLEngine
from retriever.lib.table import TabularDataset
from retriever.lib.engine_tools import json2csv, xml2csv_test


@pytest.mark.parametrize("engine_class, extension", [
    (JSONEngine, "json"),
    (XMLEngine, "xml"),
])
def test_csv_export_preserves_installed_source(tmp_path, monkeypatch, engine_class,
                                               extension):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / ("values." + extension)
    if extension == "json":
        rows = [{"name": "alpha"}, {"name": "bravo"}]
        source.write_text(json.dumps(rows), encoding="utf-8")
    else:
        source.write_text(
            "<root><row><name>alpha</name></row>"
            "<row><name>bravo</name></row></root>",
            encoding="utf-8")
    original = source.read_bytes()
    exporter = engine_class()
    exporter.encoding = "utf-8"
    exporter.script = SimpleNamespace(name="values")
    table = TabularDataset(name="values", columns=[("name", ("char",))])
    exporter.script_table_registry = {"values": [(str(source), table)]}

    for _ in range(2):
        exporter.to_csv()
        assert source.exists()
        assert source.read_bytes() == original
        with (tmp_path / "values.csv").open(newline="") as output:
            assert list(csv.reader(output)) == [["name"], ["alpha"], ["bravo"]]


@pytest.mark.parametrize("converter, extension", [(json2csv, "json"),
                                                  (xml2csv_test, "xml")])
def test_csv_converter_preserves_input(tmp_path, converter, extension):
    source = tmp_path / ("source." + extension)
    if extension == "json":
        source.write_text('{"name": "alpha"}', encoding="utf-8")
    else:
        source.write_text("<root><row><name>alpha</name></row></root>", encoding="utf-8")
    original = source.read_bytes()
    output = tmp_path / "export.csv"

    converter(str(source), str(output), header_values=["name"])

    assert source.read_bytes() == original
    with output.open(newline="") as exported:
        assert list(csv.reader(exported)) == [["name"], ["alpha"]]
