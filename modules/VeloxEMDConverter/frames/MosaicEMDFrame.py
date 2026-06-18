# -*- coding: utf-8 -*-
import customtkinter
from .MosaicSingleFrame import MosaicSingleFrame
from .MosaicMultiFrame import MosaicMultiFrame

class MosaicEMDFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabs = customtkinter.CTkTabview(self)
        self.tabs.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.SingleTab = self.tabs.add("Single mode")
        self.MultiTab = self.tabs.add("Multi mode")

        self.SingleFrame = MosaicSingleFrame(self.SingleTab)
        self.SingleFrame.pack(fill="both", expand=True)
        self.MultiFrame = MosaicMultiFrame(self.MultiTab)
        self.MultiFrame.pack(fill="both", expand=True)
    
    def reset(self): 
        self.tabs.set("Single mode")