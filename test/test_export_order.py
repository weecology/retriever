"""File-engine CSV exports must respect the requested row ordering."""
import csv
import json
from types import SimpleNamespace

import pytest

from retriever.engines.csvengine import engine as CSVEngine
from retriever.engines.jsonengine import engine as JSONEngine
from retriever.engines.xmlengine import engine as XMLEngine
from retriever.lib.table import TabularDataset


@pytest.mark.parametrize("engine_class, extension", [
    (CSVEngine, "csv"),
    (JSONEngine, "json"),
    (XMLEngine, "xml"),
])
@pytest.mark.parametrize("sort", [False, True, None])
def test_file_export_respects_sort_option(tmp_path, monkeypatch, engine_class, extension,
                                          sort):
    monkeypatch.chdir(tmp_path)
    values = ["charlie", "alpha", "bravo"]
    source = tmp_path / ("values." + extension)
    if extension == "csv":
        with source.open("w", newline="") as output:
            csv.writer(output).writerows([["name"]] + [[value] for value in values])
    elif extension == "json":
        source.write_text(json.dumps([{"name": value} for value in values]))
    else:
        source.write_text("<root>" + "".join(
            "<row><name>{}</name></row>".format(value) for value in values) + "</root>")

    exporter = engine_class()
    exporter.encoding = "utf-8"
    exporter.script = SimpleNamespace(name="values")
    table = TabularDataset(name="values", columns=[("name", ("char",))])
    exporter.script_table_registry = {"values": [(str(source), table)]}

    if sort is None:
        exporter.to_csv()
    else:
        exporter.to_csv(sort=sort)

    with (tmp_path / "values.csv").open(newline="") as output:
        rows = list(csv.reader(output))
    expected = values if sort is False else sorted(values)
    assert rows == [["name"]] + [[value] for value in expected]
