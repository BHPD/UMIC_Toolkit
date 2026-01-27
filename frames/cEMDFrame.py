# -*- coding: utf-8 -*-
import customtkinter
from frames.cEMDSidebar import cEMDSidebar 
from frames.SingleEMDFrame import SingleEMDFrame 
from frames.MosaicEMDFrame import MosaicEMDFrame

class cEMDFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        # Grid geometry of the subframes
        self.grid_columnconfigure(0, weight=0) # sidebar
        self.grid_columnconfigure(1, weight=1) # content
        self.grid_rowconfigure(0, weight=1)
        
        # Add the sidebar frame and its parameters
        self.sidebar = cEMDSidebar(self)
        self.sidebar.grid(row=0, column=0, sticky = "ns", padx=10, pady=10)
        
        # Add the content frame and its parameters
        self.single = SingleEMDFrame(self)
        self.mosaic = MosaicEMDFrame(self)
        
        # Nothing selected, comment out if single default self.select_content("single")
        
    def switch_content(self, content):
        # Reset frames
        self.single.reset()
        self.mosaic.reset()
        
        # Hide all frames
        self.single.grid_forget()
        self.mosaic.grid_forget()
        
        # Select frame
        if content == "single":
            self.single.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        elif content == "mosaic":
            self.mosaic.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Update sidebar 
        self.sidebar.highlight_button(content)