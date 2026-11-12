# -*- coding: utf-8 -*-
"""
biomero-converter module: opens the desktop GUI that ships with biomero-converter
(https://github.com/NL-BioImaging/biomero-converter, >= 0.4.0 with the [gui] extra).

Converts microscopy files (Leica, Incucyte, iSyntax, MIRAX, DICOM, .db, (OME-)TIFF,
OME-Zarr, ...) to OME-Zarr or OME-TIFF. The interface and all conversion logic live in
biomero-converter; this module only opens its window from the toolkit.
"""

# Imported here so a missing package raises ImportError when the module is opened,
# which main.py turns into an install hint instead of a crash.
from biomero_converter.gui import ConverterWindow


class BiomeroConverter(ConverterWindow):
    """The biomero-converter window, opened from the toolkit's main window."""
