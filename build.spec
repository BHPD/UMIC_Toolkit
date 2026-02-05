# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/licenses.txt', 'assets'),
        ('C:/Users/UMCG/anaconda3/envs/umic_toolkit_build/Lib/site-packages/hyperspy', 'hyperspy'),
        ('C:/Users/UMCG/anaconda3/envs/umic_toolkit_build/Lib/site-packages/rsciio', 'rsciio'),
        ('C:/Users/UMCG/anaconda3/envs/umic_toolkit_build/Lib/site-packages/box', 'box'),
    ],
    hiddenimports=[
        'xsdata_pydantic_basemodel.hooks',
        'xsdata_pydantic_basemodel.hooks.class_type'],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['box'],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    name='UMIC Toolkit v0.1.2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    onefile=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name='UMIC Toolkit v0.1.2',
)
