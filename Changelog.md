# Changelog
Changes are reported here, where X.Y.Z. correspond to:
X. Major version
Y. Minor Version
Z. Patch

### v0.2.0 (future plans)
UMIC Toolkit with a fully functional VeloxEMDConverter module.

#### Unreleased
Minor updates:
1. [NEW]        BIOMERO Converter module: GUI for biomero-converter (Leica, Incucyte, iSyntax, MIRAX, DICOM, .db, (OME-)TIFF, OME-Zarr -> OME-Zarr / OME-TIFF).
2. [CHANGE]     Modules are registered in main.py and imported only when opened, so a missing optional dependency no longer affects other modules.
3. [CHANGE]     build.spec bundles biomero-converter and its dependencies when installed in the build environment.
4. [NEW]        GitHub Actions workflow builds the Windows .exe and attaches it to each published release.
5. [NEW]        requirements.txt (tested, pinned versions) and requirements-build.txt.
6. [CHANGE]     Python 3.12 or newer is now required; main.py checks this at startup.
7. [CHANGE]     build.spec no longer contains machine-specific paths.
8. [NEW]        License notices for HyperSpy, RosettaSciIO and OpenSlide; GPL-3.0 and LGPL-2.1 texts are bundled with the .exe.
9. [NEW]        pyproject.toml with dependencies, optional extras ([biomero], [build]), Python >= 3.12 and an umic-toolkit command.
10. [CHANGE]    Version is defined once (main.__version__) and used by the window title, pyproject.toml and build.spec.
11. [CHANGE]    Removed hooks/ folder: hyperspy submodules are collected in build.spec; the ruamel.yaml hook ships with PyInstaller.
12. [NEW]       The UMIC Toolkit is licensed under GPL-3.0-or-later (LICENSE file).

#### v0.1.3 (current)
Minor updates:
1. [NEW]        Add multi-conversion for single and mosaic acquisitions where normalization is done globally for the elemental maps.
2. [CHANGE]     Renamed normal/batch (files & references) to single/multi to better reflect the underlying operation.
3. [CHANGE]     Updated auxillary files (e.g. README.md)

Bug fixes:

4. [FIX]        Single-tile OME-TIFF exports now determines and preserves input dtype.

#### v0.1.2
Minor updates:
1. [CHANGE]     Default HAADF normalization to global.
2. [CHANGE]     Indicate category in changelog.
3. [CHANGE]     Fixed some typos and aesthetics.
4. [CHANGE]     Updated README.md

Bug fixes:

5. [FIX]        Fixed crashing .exe.

#### v0.1.1
Minor updates:
1. [NEW]        Addition of Changelog.md file to reflect changes between versions.
2. [CHANGE]     No 'export' folder will be automatically created anymore when using mosaic conversion.
3. [UPDATE]     Stitching window is updated with information on how to stitch the exported .tiffs in TrakEM2.
4. [NEW]        Added choice to use local or global normalization for the HAADF.
5. [NEW]        Update status bar with information on current stage in processing.
6. [UPDATE]     Change name of VeloxEMDProcessor to VeloxEMDConverter.
7. [CHANGE]     Frames no longer reset after switching to another frame.
8. [NEW]        Retain all 'original_metadata' from each .emd in each .tiff individually.
9. [NEW]        Added conversion from TrakEM2 export to OME-TIFF.

Bug fixes:

10. [FIX]       Data files within the .emd with titles in ['a'] will now be excluded

Known bugs:

11. [BUG]       Something may still be wrong with the OME-XML.

#### v0.1.0
Re-organization of file structure and changes of files for the purpose of:
1. [NEW]        Creation of UMIC Toolkit GUI
2. [CHANGE]     Conversion of original VeloxEMDProcessor GUI to a CTk.Toplevel window
3. [CHANGE]     Addition of VeloxEMDProcessor as a module to UMIC Toolkit GUI
