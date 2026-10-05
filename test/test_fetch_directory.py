"""Fetch must install and read its SQLite database in the same directory."""
import importlib

import pytest

from retriever.lib.table import TabularDataset
from retriever.lib.templates import BasicTextTemplate

install_module = importlib.import_module("retriever.lib.install")
fetch_module = importlib.import_module("retriever.lib.fetch")


@pytest.mark.parametrize("custom_directory", [True, False])
def test_fetch_uses_requested_data_directory(tmp_path, monkeypatch, custom_directory):
    monkeypatch.chdir(tmp_path)
    directory = tmp_path / "data" if custom_directory else tmp_path
    directory.mkdir(exist_ok=True)

    source = tmp_path / "source.csv"
    source.write_text("name\nAlex\n", encoding="utf-8")
    table = TabularDataset(name="values",
                           url=source.as_uri(),
                           path=str(source),
                           format="tabular",
                           delimiter=",",
                           columns=[("name", ("char",))])
    script = BasicTextTemplate(name="sample", tables={"values": table})
    monkeypatch.setattr(install_module, "SCRIPT_LIST", lambda: [script])
    options = {"data_dir": str(directory)} if custom_directory else {}

    frames = fetch_module.fetch("sample", file="sample.db", **options)

    assert frames["values"].to_dict("list") == {"name": ["Alex"]}
    assert (directory / "sample.db").is_file()
    if custom_directory:
        assert not (tmp_path / "sample.db").exists()
