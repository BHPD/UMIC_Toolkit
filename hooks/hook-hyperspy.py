# Force PyInstaller to import Hyperspy so it registers the package root
#import hyperspy

from PyInstaller.utils.hooks import collect_submodules

hiddenimports = (
    collect_submodules('hyperspy') +
    collect_submodules('rsciio') +
    collect_submodules('box')
)
