"""JSON object key order must not determine CSV column alignment."""
import csv
import json

import pytest

from retriever.lib.engine_tools import json2csv


@pytest.mark.parametrize("data, row_key, header", [
    ({
        "age": 25,
        "name": "Alex"
    }, None, ["name", "age"]),
    ([{
        "age": 25,
        "name": "Alex"
    }, {
        "name": "Ben",
        "age": 24
    }], None, ["name", "age"]),
    ({
        "results": [{
            "age": 25,
            "name": "Alex"
        }]
    }, "results", ["name", "age"]),
    ({
        "age": 25,
        "name": "Alex",
        "unused": "ignored"
    }, None, ["name", "age"]),
])
def test_json2csv_aligns_values_with_headers(tmp_path, data, row_key, header):
    source = tmp_path / "data.json"
    output = tmp_path / "data.csv"
    source.write_text(json.dumps(data), encoding="utf-8")

    json2csv(str(source), str(output), header_values=header, row_key=row_key)

    expected = [header, ["Alex", "25"]]
    if isinstance(data, list):
        expected.append(["Ben", "24"])
    with output.open(encoding="utf-8", newline="") as csv_file:
        assert list(csv.reader(csv_file)) == expected
