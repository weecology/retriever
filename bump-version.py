from fileinput import FileInput
import sys
import re

if len (sys.argv) != 2 :
    print("Usage: python bump-version.py 3.2.1")
    sys.exit (1)
arg = sys.argv[1]

file_list =[ 
    "retriever/_version.py",
    "retriever_installer.iss",
    "setup.py",
    
]


with FileInput(files=file_list, inplace=True) as f:
    for line in f:
        if re.match("\AAppVersion=", line):
            line = "AppVersion="+arg
            print(line) 
        elif re.match("\A__version__ =", line):
            line = "__version__ = "+"\'v"+arg+"\'"
            print(line) 
        else:
            print(line,end='')

with FileInput(files=["version.txt"], inplace=True) as f:
    for line in f:
        if re.match("\Av{1}\d+\.\d+\.\d+", line):
            line = "v"+arg
            print(line)
        else:
            print(line,end='')