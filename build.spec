# -*- mode: python ; coding: utf-8 -*-

import os, re, importlib.util

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

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/licenses.txt', 'assets'),
        ('assets/third_party', 'third_party'),
        ('modules/VeloxEMDConverter/frames/StitchInfo.txt', '.'),
        (package_dir('hyperspy'), 'hyperspy'),
        (package_dir('rsciio'), 'rsciio'),
        (package_dir('box'), 'box'),
    ],
    hiddenimports=[
        'xsdata_pydantic_basemodel.hooks',
        'xsdata_pydantic_basemodel.hooks.class_type'] + module_imports,
    hookspath=['hooks'],  # hook-hyperspy.py; biomero-converter (>=0.2.4) ships its own hook
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
