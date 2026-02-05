import os,  sys, customtkinter
from modules.VeloxEMDConverter.VeloxEMDConverter import VeloxEMDConverter
from assets.load_licenses import license_window

customtkinter.set_appearance_mode("dark") 
customtkinter.set_default_color_theme("dark-blue")

class UMICToolkit(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("UMIC Toolkit v0.1.2")
        self.geometry("320x360")

        self.content = customtkinter.CTkFrame(self)
        self.content.pack(fill="both", expand=True, padx=20, pady=20)

        self.vEMDConverter_btn = customtkinter.CTkButton(self.content,
                                                         text = "Velox EMD Converter",
                                                         command = self.open_vEMDConverter)
        self.vEMDConverter_btn.grid(row=0, column=0,  sticky='nsew', pady=5, padx =5)

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
            
    def open_vEMDConverter(self):
        vEMD_window = VeloxEMDConverter(self)

if __name__ == "__main__":
    app = UMICToolkit()
    app.mainloop()