import os, sys, customtkinter

class StitchFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        StitchInfoPath = self.file_path("StitchInfo.txt")
        try:
            with open(StitchInfoPath, "r", encoding="utf-8") as f:
                info_text = f.read()
        except Exception as e:
            info_text = f"Could not load stitch info file:\n{e}"
    
        # Make scrollable frame
        self.info_frame = customtkinter.CTkScrollableFrame(self)
        self.info_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Grid geometry of the subframes
        self.info=customtkinter.CTkLabel(
            self.info_frame, 
            text=info_text,
            anchor='w',
            font = ("Courier New", 12),
            justify = "left")
        #self.info.grid(row=0, column=0, sticky = "new", padx=10, pady=10)
        self.info.pack(anchor = 'w', fill = 'both', expand = True)

    def file_path(self, relative_path):
    # for PyInstaller
        if hasattr(sys, 'frozen'):
            base_path = sys._MEIPASS
        # for development
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)