# -*- coding: utf-8 -*-
import customtkinter
from .frames.MainTabs import MainTabs

class VeloxEMDConverter(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        
        # Standard GUI parameters
        self.title('Velox EMD Converter')
        self.geometry("1280x720")
        self.transient(master)
        self.lift()
        self.focus_force()


        # Grid geometry of the main app
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Main tabs
        self.tabs = MainTabs(self)
        self.tabs.pack(fill="both", expand=True)

