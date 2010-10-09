rmdir %~dp0current-release\windows /s
mkdir %~dp0current-release\windows
cd %~dp0current-release\src\dbtk
python setup.py py2exe
move dist\main.exe %~dp0current-release\windows
rmdir build dist /s
ren %~dp0current-release\windows\main.exe dbtk.exe
