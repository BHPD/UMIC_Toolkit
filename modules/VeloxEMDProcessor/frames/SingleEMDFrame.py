# -*- coding: utf-8 -*-
import customtkinter
from .SingleNormalFrame import SingleNormalFrame
from .SingleBatchFrame import SingleBatchFrame

class SingleEMDFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabs = customtkinter.CTkTabview(self)
        self.tabs.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.NormalTab = self.tabs.add("Normal mode")
        self.BatchTab = self.tabs.add("Batch mode")

        self.NormalFrame = SingleNormalFrame(self.NormalTab)
        self.NormalFrame.pack(fill="both", expand=True)
        self.BatchFrame = SingleBatchFrame(self.BatchTab)
        self.BatchFrame.pack(fill="both", expand=True)
    
    def reset(self): 
        self.tabs.set("Normal mode")
        self.NormalFrame.reset()
        self.BatchFrame.reset()