# -*- coding: utf-8 -*-
import customtkinter

class SingleBatchFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        customtkinter.CTkLabel(self, text='Batch mode!').pack()