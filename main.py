# -*- coding: utf-8 -*-
import customtkinter
from frames.MainTabs import MainTabs
from assets.load_licenses import license_window

customtkinter.set_appearance_mode("dark") 
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # Standard GUI parameters
        self.title('Velox EMD Processor v0.1')
        self.geometry("1280x720")
        
        # Grid geometry of the main app
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Main tabs
        self.tabs = MainTabs(self)
        self.tabs.pack(fill="both", expand=True)

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

if __name__ == "__main__":
    app = App()
    app.mainloop()