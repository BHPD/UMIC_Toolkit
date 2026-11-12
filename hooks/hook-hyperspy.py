# PyInstaller hook for HyperSpy (used by the Velox EMD Converter module).
# HyperSpy and RosettaSciIO load submodules dynamically (signal types, plugins,
# IO readers), so include all their submodules.
# (python-box is excluded from analysis and shipped as a plain folder, see build.spec.)
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules('hyperspy') + collect_submodules('rsciio')
