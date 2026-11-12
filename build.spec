# -*- mode: python ; coding: utf-8 -*-

import os, re, importlib.util
from PyInstaller.utils.hooks import collect_all, collect_submodules

# Name of the build (folder + exe). CI passes the release tag via UMIC_VERSION;
# otherwise the version is read from main.py (__version__).
with open('main.py', encoding='utf-8') as f:
    _version = re.search(r'__version__\s*=\s*"([^"]+)"', f.read()).group(1)
app_name = 'UMIC Toolkit ' + os.environ.get('UMIC_VERSION', 'v' + _version)


def package_dir(pkg):
    # Location of an installed package, so no machine-specific paths are needed.
    return os.path.dirname(importlib.util.find_spec(pkg).origin)


block_cipher = None

# Toolkit modules are imported lazily from main.py (importlib), so PyInstaller
# cannot discover them by itself: list them explicitly here.
module_imports = [
    'modules.VeloxEMDConverter.VeloxEMDConverter',
    'modules.BiomeroConverter.BiomeroConverter',
]

# HyperSpy and RosettaSciIO load submodules dynamically (plugins, IO readers),
# so include all their submodules. (Previously hooks/hook-hyperspy.py.)
# python-box is excluded from analysis and shipped as a plain folder (see datas).
dynamic_imports = (collect_submodules('hyperspy') +
                   collect_submodules('rsciio'))

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
        ('assets/third_party', 'third_party'),
        ('modules/VeloxEMDConverter/frames/StitchInfo.txt', '.'),
        (package_dir('hyperspy'), 'hyperspy'),
        (package_dir('rsciio'), 'rsciio'),
        (package_dir('box'), 'box'),
    ] + extra_datas,
    hiddenimports=[
        'xsdata_pydantic_basemodel.hooks',
        'xsdata_pydantic_basemodel.hooks.class_type'] + module_imports + dynamic_imports + extra_hiddenimports,
    hookspath=[],
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
    name=app_name,
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
    name=app_name,
)
