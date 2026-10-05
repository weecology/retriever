"""XML export must round-trip text without treating it as markup."""
import xml.etree.ElementTree as ET
from types import SimpleNamespace

import pytest

from retriever.engines.xmlengine import engine, format_single_row
from retriever.lib.table import TabularDataset


@pytest.mark.parametrize("value", [
    "fish & wildlife",
    "temperature < 20",
    "</name><injected>not markup</injected><name>",
    "literal &amp; entity",
    'quotes " and apostrophes \u0027',
    "caf\u00e9 > tea",
    25,
    "",
])
def test_xml_export_preserves_field_text(value):
    serialized = format_single_row(["name"], [value])

    row = ET.fromstring("<row>" + serialized + "</row>")

    assert [child.tag for child in row] == ["name"]
    assert (row[0].text or "") == str(value)


def test_xml_engine_exports_parseable_file(tmp_path):
    exporter = engine()
    exporter.opts = {"data_dir": str(tmp_path), "table_name": "{table}.xml"}
    exporter.encoding = "utf-8"
    exporter.table = TabularDataset(name="values", columns=[("name", ("char",))])
    exporter.script = SimpleNamespace(name="values")
    exporter.table_names = []
    exporter.script_table_registry = {}
    values = [["fish & wildlife"], ["temperature < 20"], ["literal &amp; entity"]]

    exporter.create_table()
    exporter.execute(exporter.insert_statement(values))
    exporter.disconnect()

    root = ET.parse(tmp_path / "values.xml").getroot()
    assert [[child.text for child in row] for row in root] == values
