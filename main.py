import os, sys, importlib, customtkinter

__version__ = "0.1.3"  # single source of the version (pyproject.toml and build.spec read it)
from tkinter import messagebox

MIN_PYTHON = (3, 12)
if sys.version_info < MIN_PYTHON:
    sys.exit(f"UMIC Toolkit requires Python {'.'.join(map(str, MIN_PYTHON))} or newer "
             f"(found {sys.version.split()[0]}).")

from assets.load_licenses import license_window

# Registry of toolkit modules: (button label, module path, class name, install hint).
# Modules are imported only when opened, so a missing optional dependency
# (e.g. biomero-converter) does not prevent the other modules from working.
MODULES = [
    ("Velox EMD Converter", "modules.VeloxEMDConverter.VeloxEMDConverter", "VeloxEMDConverter",
     None),
    ("BIOMERO Converter", "modules.BiomeroConverter.BiomeroConverter", "BiomeroConverter",
     "pip install biomero-converter"),
]

customtkinter.set_appearance_mode("dark") 
customtkinter.set_default_color_theme("dark-blue")

class UMICToolkit(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"UMIC Toolkit v{__version__}")
        self.geometry("320x360")

        self.content = customtkinter.CTkFrame(self)
        self.content.pack(fill="both", expand=True, padx=20, pady=20)

        for row, (label, mod_path, cls_name, hint) in enumerate(MODULES):
            btn = customtkinter.CTkButton(
                self.content,
                text=label,
                command=lambda m=mod_path, c=cls_name, h=hint: self.open_module(m, c, h))
            btn.grid(row=row, column=0, sticky='nsew', pady=5, padx=5)

        self.content.grid_columnconfigure('all', weight=1) 
        self.content.grid_rowconfigure('all', weight=0)

        # Bottom bar containing the info and mode-switch
        self.bottom_bar = customtkinter.CTkFrame(self)
        self.bottom_bar.pack(side="bottom", fill="x", padx=10, pady=10)

        # Light/Dark mode switch
        self.theme_switch = customtkinter.CTkSwitch(
            self.bottom_bar,
            text="Dark mode",
            command=self.toggle_theme
        )
        self.theme_switch.select()
        self.theme_switch.pack(side="left", padx=(0, 10))

        # Licenses button
        self.license_btn = customtkinter.CTkButton(
            self.bottom_bar,
            text="License and information ⓘ",
            width=50,
            command=lambda: license_window(self)
        )
        self.license_btn.pack(side="right", padx=(0, 10))

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            customtkinter.set_appearance_mode("dark")
            self.theme_switch.configure(text="Dark mode")
        else:
            customtkinter.set_appearance_mode("light")
            self.theme_switch.configure(text="Light mode")
            
    def open_module(self, mod_path, cls_name, install_hint=None):
        try:
            cls = getattr(importlib.import_module(mod_path), cls_name)
        except ImportError as e:
            msg = f"This module could not be loaded:\n{e}"
            if install_hint:
                msg += f"\n\nInstall the required package with:\n{install_hint}"
            messagebox.showerror("Module unavailable", msg, parent=self)
            return
        cls(self)

def run():
    app = UMICToolkit()
    app.mainloop()

if __name__ == "__main__":
    run()