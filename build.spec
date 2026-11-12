# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Toolkit modules are imported lazily from main.py (importlib), so PyInstaller
# cannot discover them by itself: list them explicitly here.
module_imports = [
    'modules.VeloxEMDConverter.VeloxEMDConverter',
    'modules.BiomeroConverter.BiomeroConverter',
]

# Optional: bundle biomero-converter and its dependencies (data files, native
# libraries such as OpenSlide, codecs) when it is installed in the build env.
extra_datas, extra_binaries, extra_hiddenimports = [], [], []
for pkg in ('biomero_converter', 'openslide', 'openslide_bin', 'imagecodecs',
            'ome_zarr', 'zarr', 'numcodecs', 'pyisyntax', 'pydicom', 'rocrate', 'liffile'):
    try:
        d, b, h = collect_all(pkg)
    except Exception:
        continue
    extra_datas += d
    extra_binaries += b
    extra_hiddenimports += h

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=extra_binaries,
    datas=[
        ('assets/licenses.txt', 'assets'),
        ('modules/VeloxEMDConverter/frames/StitchInfo.txt', '.'),
        ('C:/Users/UMCG/anaconda3/envs/umic_toolkit_build/Lib/site-packages/hyperspy', 'hyperspy'),
        ('C:/Users/UMCG/anaconda3/envs/umic_toolkit_build/Lib/site-packages/rsciio', 'rsciio'),
        ('C:/Users/UMCG/anaconda3/envs/umic_toolkit_build/Lib/site-packages/box', 'box'),
    ] + extra_datas,
    hiddenimports=[
        'xsdata_pydantic_basemodel.hooks',
        'xsdata_pydantic_basemodel.hooks.class_type'] + module_imports + extra_hiddenimports,
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
    name='UMIC Toolkit v0.1.3',
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
    name='UMIC Toolkit v0.1.3',
)
