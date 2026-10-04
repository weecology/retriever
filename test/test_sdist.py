"""Check that source archives contain the files needed to run the tests."""
import shutil
import tarfile
from pathlib import Path

from setuptools import Distribution


def test_sdist_contains_test_fixtures(tmp_path, monkeypatch):
    source = Path(__file__).resolve().parents[1]
    root = tmp_path / "source"
    root.mkdir()
    for name in ("MANIFEST.in", "setup.py", "README.md", "CITATION", "LICENSE",
                 "requirements.txt"):
        shutil.copyfile(source / name, root / name)
    shutil.copytree(source / "test",
                    root / "test",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"))
    expected = {
        path.relative_to(root).as_posix()
        for path in (root / "test").rglob("*")
        if path.is_file()
    }
    cache = root / "test" / "__pycache__"
    cache.mkdir()
    (cache / "test_sdist.cpython-311.pyc").write_bytes(b"cached bytecode")
    monkeypatch.chdir(root)

    # Exercise the manifest without running setup.py's installation bootstrap.
    distribution = Distribution({
        "name": "manifest-test",
        "version": "0.0",
        "script_name": "setup.py"
    })
    command = distribution.get_command_obj("sdist")
    command.dist_dir = str(tmp_path / "dist")
    command.ensure_finalized()
    command.run()

    with tarfile.open(command.archive_files[0]) as archive:
        files = {
            member.name.split("/", 1)[1]
            for member in archive.getmembers()
            if member.isfile()
        }
    assert expected <= files
    assert not any(
        "__pycache__" in path or path.endswith((".pyc", ".pyo")) for path in files)
