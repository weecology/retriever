# -*- mode: python -*-
import os
import distutils.util

platform = distutils.util.get_platform()
block_cipher = None

a = Analysis([os.path.normpath('retriever/__main__.py')],
             pathex=['.', 'lib','engines', 'scripts'],
             binaries=[],
             datas=[],
             hiddenimports=['xlrd', 'pymysql', 'psycopg2', 'sqlite3', 'pyodbc'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[
                       ],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.pure += [('retriever.engines.mysql','retriever/engines/mysql.py','PYMODULE'),
           ('retriever.engines.postgres','retriever/engines/postgres.py', 'PYMODULE'),
           ('retriever.engines.sqlite','retriever/engines/sqlite.py', 'PYMODULE'),
           ('retriever.engines.msaccess','retriever/engines/msaccess.py', 'PYMODULE'),
           ('retriever.engines.csvengine','retriever/engines/csvengine.py', 'PYMODULE'),
           ('retriever.engines.download_only','retriever/engines/download_only.py', 'PYMODULE'),
           ('retriever.engines.jsonengine','retriever/engines/jsonengine.py', 'PYMODULE'),
           ('retriever.engines.xmlengine','retriever/engines/xmlengine.py', 'PYMODULE'),
           ('retriever.lib.templates', 'retriever/lib/templates.py', 'PYMODULE'),
           ('retriever.lib.excel', 'retriever/lib/excel.py', 'PYMODULE'),
           ('retriever.lib.dummy', 'retriever/lib/dummy.py', 'PYMODULE')
           ]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

icon_file='icon.ico'
if 'macosx' in platform:
    icon_file='osx_icon.icns'

if 'macosx' or 'linux' in platform:
    exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            name='retriever',
            debug=False,
            strip=False,
            upx=True,
            console=False , icon=icon_file)

if 'macosx' in platform:
    app = BUNDLE(exe,
               name='retriever.app',
               icon='osx_icon.icns',
               bundle_identifier=None)

if 'win' in platform:
    exe = EXE(pyz,
              a.scripts,
              exclude_binaries=True,
              name='retriever',
              debug=False,
              strip=False,
              upx=True,
              console=True,  icon=icon_file )
    coll = COLLECT(exe,
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   strip=False,
                   upx=True,
                   name='packages')
