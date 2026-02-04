# -*- coding: utf-8 -*-
import customtkinter

class MosaicBatchFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        customtkinter.CTkLabel(self, text='Batch mode!').pack()