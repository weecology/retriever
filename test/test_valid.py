import json
from glob import glob


def test_valid_json():
    """Test if all json files are valid"""
    for filename in glob("./scripts/*.json"):
        assert "-" not in filename
        with open(filename, "r") as fin:
            assert json.load(fin)


def test_valid_python():
    """Test if all python files have valid names"""
    for filename in glob("./scripts/*.py"):
        assert "-" not in filename
