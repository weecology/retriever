"""Sorting CSV files must preserve complete records and field values."""
import csv

import pytest

from retriever.lib.engine_tools import sort_csv


@pytest.mark.parametrize("rows", [
    [["Ben", "zulu\nAAA"], ["Alex", "first"]],
    [["Ben", "line one\r\nline two"], ["Alex", "first"]],
    [["Ben", "trailing spaces  "], ["Alex", 'commas, quotes " and \\']],
    [["Alex", "US"], ["Ben", "US"], ["Alex", "PT"]],
    [],
])
def test_sort_csv_preserves_records(tmp_path, rows):
    path = tmp_path / "data.csv"
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output, escapechar="\\")
        writer.writerow(["name", "notes"])
        writer.writerows(rows)

    assert sort_csv(str(path)) == str(path)

    with path.open(encoding="utf-8", newline="") as source:
        assert list(csv.reader(source,
                               escapechar="\\")) == [["name", "notes"]] + sorted(rows)


def test_sort_csv_leaves_unrelated_tempfile_untouched(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    temporary = tmp_path / "tempfile"
    temporary.write_text("existing data", encoding="utf-8")
    path = tmp_path / "data.csv"
    path.write_text("name\nBen\nAlex\n", encoding="utf-8")

    sort_csv(str(path))

    assert temporary.read_text(encoding="utf-8") == "existing data"


def test_sort_csv_accepts_empty_file(tmp_path):
    path = tmp_path / "data.csv"
    path.touch()

    sort_csv(str(path))

    assert path.read_bytes() == b""
