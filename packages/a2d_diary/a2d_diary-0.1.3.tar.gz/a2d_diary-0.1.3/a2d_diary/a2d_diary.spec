# -*- mode: python -*-

block_cipher = None


a = Analysis(['a2d_diary.py'],
             pathex=['C:\\Users\\julio\\Documents\\phd\\skip\\src\\diary\\a2d-diary\\src'],
             binaries=[],
             datas=[(r'C:\Users\julio\Documents\phd\skip\src\diary\a2d-diary\src\static', 'static'),
                    (r'C:\Users\julio\Documents\phd\skip\src\diary\a2d-diary\src\input', 'input'),
                    (r'C:\Users\julio\Documents\phd\skip\src\diary\a2d-diary\src\output', 'output')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='A2D_Diary',
          debug=False,
          strip=False,
          upx=False,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='a2d_diary')
