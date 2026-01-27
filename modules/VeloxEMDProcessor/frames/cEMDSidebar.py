# -*- coding: utf-8 -*-
import customtkinter

class cEMDSidebar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.parent = master
        
        # Apply theme colors
        self.active_color = customtkinter.ThemeManager.theme["CTkSegmentedButton"]["selected_color"]
        self.inactive_color = customtkinter.ThemeManager.theme["CTkSegmentedButton"]["fg_color"]
            
        # Sidebar grid geometry
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        
        # Add buttons
        self.single_btn = customtkinter.CTkButton(
            self,
            text = 'Single',
            fg_color=self.inactive_color,
            command=lambda: self.parent.switch_content('single'))

        self.mosaic_btn = customtkinter.CTkButton(
            self,
            text = 'Mosaic',
            fg_color=self.inactive_color,
            command=lambda: self.parent.switch_content('mosaic'))
        
        self.single_btn.grid(row=0, column = 0, sticky = 'nsew', pady = 5)
        self.mosaic_btn.grid(row=1, column = 0, sticky = 'nsew', pady = 5)

    def highlight_button(self, active): 
        self.single_btn.configure(fg_color=self.active_color 
                                  if active == "single" 
                                  else self.inactive_color ) 
        self.mosaic_btn.configure(fg_color=self.active_color 
                                  if active == "mosaic" 
                                  else self.inactive_color )