# Changelog
Changes are reported here, where X.Y.Z. correspond to:
X. Major version
Y. Minor Version
Z. Patch

### v0.2.0 (future plans)
UMIC Toolkit with a fully functional VeloxEMDProcessor module.

#### v0.1.1 (current)
Minor changes:
1. Addition of Changelog.md file to reflect changes between versions.
2. No 'export' folder will be automatically created anymore when using mosaic conversion.
3. Stitching window is updated with information on how to stitch the exported .tiffs in TrakEM2.
4. Added choice to use local or global normalization for the HAADF.
5. Update status bar with information on current stage in processing.
6. Change name of VeloxEMDProcessor to VeloxEMDConverter.
7. Frames no longer reset after switching to another frame.
8. Retain all 'original_metadata' from each .emd in each .tiff individually.
9. Added TrakEM2 project to OME-TIFF conversion

Bug fixes:
9. OK. Data files within the .emd with titles in ['a'] will now be excluded

Known bugs:
10. Something may still be wrong with the OME-XML.

#### v0.1.0
Re-organization of file structure and changes of files for the purpose of:
1. Creation of UMIC Toolkit GUI
2. Conversion of original VeloxEMDProcessor GUI to a CTk.Toplevel window
3. Addition of VeloxEMDProcessor as a module to UMIC Toolkit GUI
