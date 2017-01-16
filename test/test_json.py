import json
import os

HOMEDIR = os.path.expanduser('~')
file_location = os.path.dirname(os.path.realpath(__file__))
retriever_root_dir = os.path.abspath(os.path.join(file_location, os.pardir))

def json_test_module():
	"""Test if all json files are valid"""
	os.chdir(retriever_root_dir + '/scripts')
	for filename in os.listdir("."):
		if filename[-5:] == ".json":
			file_content = ""
			with open(filename, "r") as fin:
				assert json.load(fin)
