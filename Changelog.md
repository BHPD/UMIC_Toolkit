# Changelog
Changes are reported here, where X.Y.Z. correspond to:
X. Major version
Y. Minor Version
Z. Patch

### v0.2.0 (future plans)
UMIC Toolkit with a fully functional VeloxEMDConverter module.

#### v0.1.2 (current)
Minor updates:
1. [CHANGE]     Default HAADF normalization to global.
2. [CHANGE]     Indicate category in changelog.
3. [CHANGE]     Fixed some typos and aesthetics.
4. [CHANGE]     Updated README.md

Bug fixes:
4. [FIX]        Fixed crashing .exe.

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
