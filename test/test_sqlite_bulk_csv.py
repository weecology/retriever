"""SQLite bulk insertion must parse CSV records rather than split lines."""
import csv
from types import SimpleNamespace

import pytest

from retriever.engines.sqlite import engine
from retriever.lib.table import TabularDataset


@pytest.mark.parametrize("values", [
    ["quoted, comma", 'a "quoted" word'],
    ["first line\nsecond line", "ordinary"],
    ['a "quoted" word', ""],
    ["plain", "another"],
    [str(i) for i in range(1005)],
])
def test_sqlite_bulk_insert_preserves_csv_values(tmp_path, values):
    source = tmp_path / "input.csv"
    with source.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(["value"])
        writer.writerows([[value] for value in values])
    importer = engine()
    importer.opts = {
        "data_dir": str(tmp_path),
        "file": "data.db",
        "table_name": "{db}_{table}"
    }
    importer.table = TabularDataset(name="values",
                                    delimiter=",",
                                    columns=[("value", ("char",))])
    importer.script = SimpleNamespace(name="sample", encoding="utf-8", tables={})
    importer.script_table_registry = {}
    importer.create_table()

    try:
        assert importer.insert_data_from_file(str(source)) is True
        actual = importer.cursor.execute("SELECT value FROM sample_values ORDER BY rowid")
        assert [row[0] for row in actual] == values
    finally:
        importer.disconnect()
