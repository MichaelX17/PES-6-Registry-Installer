# -*- mode: python -*-
import os  # Asegúrate de importar os

block_cipher = None

# Usa el directorio actual en lugar de __file__
script_dir = os.getcwd()

a = Analysis(
    ['pes6_reg_editor.py'],
    pathex=[script_dir],  # Ruta dinámica
    binaries=None,
    datas=[('pes6.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher
)

# El resto del código se mantiene igual...
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='pes6_reg_editor',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='pes6.ico')