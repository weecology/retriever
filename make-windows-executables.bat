rmdir %~dp0current-release\windows /s
mkdir %~dp0current-release\windows
cd %~dp0current-release\srcretriever
python setup.py py2exe
move dist\retriever.exe %~dp0current-release\windows
rmdir build dist /s
del __init__.pyc