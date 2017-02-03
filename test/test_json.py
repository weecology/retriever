import json
from glob import glob


def test_valid_json():
    """Test if all json files are valid"""
    for filename in glob("./scripts/*.json"):
        with open(filename, "r") as fin:
            assert json.load(fin)
