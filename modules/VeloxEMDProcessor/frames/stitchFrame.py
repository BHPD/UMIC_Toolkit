# -*- coding: utf-8 -*-
import customtkinter

class stitchFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # Grid geometry of the subframes
        self.info=customtkinter.CTkLabel(
            self, 
            text='Use TrakEM2 to stitch: \n' +
            '1. Step 1 \n' +
            '2. Step 2 \n' +
            '... and so forth, actuals steps will follow',
            anchor='center')
        self.info.grid(row=0, column=0, sticky = "new", padx=10, pady=10)