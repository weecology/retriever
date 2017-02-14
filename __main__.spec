# -*- mode: python -*-

block_cipher = None


a = Analysis(['__main__.py'],
             pathex=['.', 'lib','engines', 'scripts'],
             binaries=[],
             datas=[],
             hiddenimports=['xlrd'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.pure += [('retriever.engines.mysql','engines/mysql.py','PYMODULE'),
           ('retriever.engines.postgres','engines/postgres.py', 'PYMODULE'),
           ('retriever.engines.sqlite','engines/sqlite.py', 'PYMODULE'),
           ('retriever.engines.msaccess','engines/msaccess.py', 'PYMODULE'),
           ('retriever.engines.csvengine','engines/csvengine.py', 'PYMODULE'),
           ('retriever.engines.download_only','engines/download_only.py', 'PYMODULE'),
           ('retriever.engines.jsonengine','engines/jsonengine.py', 'PYMODULE'),
           ('retriever.engines.xmlengine','engines/xmlengine.py', 'PYMODULE'),
           ('retriever.lib.templates', 'lib/templates.py', 'PYMODULE'),
           ('retriever.lib.excel', 'lib/excel.py', 'PYMODULE')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='retriever',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='packages')
