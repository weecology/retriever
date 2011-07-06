rmdir %~dp0windows /s
mkdir %~dp0windows
python setup.py py2exe
move dist\retriever.exe %~dp0windows
rmdir build dist /s