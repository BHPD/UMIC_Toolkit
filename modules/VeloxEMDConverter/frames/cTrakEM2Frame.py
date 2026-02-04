import customtkinter, threading, gc, time
from tkinter import filedialog
from ..utils import base_functions as bf

class cTrakEM2Frame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Initialisation
        self.file_input_path=None # Placeholder for the input path
        self.file_export_path=None # Placeholder for the export path
        self.metadata_path=None # Placeholder for the metadata path

        # Grid geometry weights
        self.grid_columnconfigure(0, weight=1)  # Spread the selected file/folder
        self.grid_rowconfigure((0,1,2,3,4), weight=1)  # Push options + conversion to bottom.
        
        # Row 0, info text
        self.info=customtkinter.CTkLabel(
            self, 
            text='Process a TrakEM2 project' +
            '\nExports stitched .tiffs generated using TrakEM2',
            anchor='center')
        self.info.grid(row=0, column=0, columnspan=4, sticky='new', pady=5, padx =5)

        # Row 1, selected file (input)
        self.file_input=customtkinter.CTkLabel(
            self,
            text='Input folder',
            anchor='w')
        self.file_input.grid(row=1, column=0, sticky='w', pady=5, padx =5)

        # Row 1, browse button (input)
        self.browse_input=customtkinter.CTkButton(
            self,
            text='Browse',
            command=self.browse_input)
        self.browse_input.grid(row=1, column=3, sticky='ew', pady=5, padx =5)
        
        # Row 2, selected folder (export)
        self.file_export=customtkinter.CTkLabel(
            self,
            text=r'Export folder',
            anchor='w')
        self.file_export.grid(row=2, column=0, sticky='w', pady=5, padx =5)

        # Row 2, browse button (export)
        self.browse_export=customtkinter.CTkButton(
            self,
            text='Browse',
            command=self.browse_export)
        self.browse_export.grid(row=2, column=3, sticky='ew', pady=5, padx =5)

        # Row 3, selected file (metadata)
        self.file_metadata=customtkinter.CTkLabel(
            self,
            text=r'Metadata file: FIRST .tiff from ANY of the exported element map folders',
            anchor='w')
        self.file_metadata.grid(row=3, column=0, sticky='w', pady=5, padx =5)
        
        # Row 3, browse file (metadata)
        self.browse_export=customtkinter.CTkButton(
            self,
            text='Browse',
            command=self.browse_metadata)
        self.browse_export.grid(row=3, column=3, sticky='ew', pady=5, padx =5)

        # Row 4, empty weighted row to force the options & conversion down in the frame

        # Row 5, Filename
        self.info_filename = customtkinter.CTkLabel(
            self,
            text='Export filename:',
            anchor='w').grid(row=5, column=2, sticky='w', pady=5, padx =5)
    
        self.options_filename = customtkinter.CTkEntry(
            self,
            placeholder_text =  'Type filename here')
        self.options_filename.grid(row=5, column=3, sticky='we', pady=5, padx =5)

        # Row 6, File-type selection
        self.info_filetype = customtkinter.CTkLabel(
            self,
            text='File type:',
            anchor='w').grid(row=6, column=2, sticky='w', pady=5, padx =5)

        self.options_filetype=customtkinter.CTkOptionMenu(
            self,
            values=['OME-TIFF'],
            anchor='s') 
        self.options_filetype.grid(row=6, column=3, sticky='wes', pady=5, padx =5)
        
        # Row 7, room for pop-up information
        self.popup=customtkinter.CTkLabel(
            self,
            text=None,
            anchor='s')
        self.popup.grid(row=7, column=0, columnspan=4, sticky='wes', pady=5, padx =5)        

        # Row 8, convert button
        customtkinter.CTkButton(
            self,
            text='Convert',
            anchor='s',
            command=self.convert
        ).grid(row=8, column=0,  columnspan=4, sticky='wes', pady=5, padx =5)

        # Row 9, indeterminate progress bar
        self.progress=customtkinter.CTkProgressBar(
            self, 
            mode='indeterminate',
            height=5,
            corner_radius=1,
            progress_color='green')
        self.progress.grid(row=9, column=0, columnspan=4, sticky='wes', pady=5, padx =5)
        self.progress.stop()

    def browse_input(self):
        path=filedialog.askdirectory()
        if path:
            self.file_input_path=path
            self.file_input.configure(text=path)
    
    def browse_export(self):
        path=filedialog.askdirectory()
        if path:
            self.file_export_path=path
            self.file_export.configure(text=path)

    def browse_metadata(self):
        path=filedialog.askopenfilename()
        if path:
            self.file_metadata_path=path
            self.file_metadata.configure(text=path)

    def convert(self):
        start_time = time.time()
        def task():
            self.progress.start()
            bf.tiffFolderToOmeTiff(self,
                             self.file_input_path, 
                             self.file_export_path,
                             self.options_filename.get(),
                             self.file_metadata_path)
            self.progress.stop()
            self.progress.set(1)
            self.popup.configure(text='Completed! \n'+ 
                                 f'Took {(time.time() - start_time):.2f} seconds.')
            gc.collect()
        if not self.file_export_path or not self.file_input_path or not self.file_metadata_path:
            self.popup.configure(text='Select an import folder, export folder and/or a metadata file!')
            return    
        
        threading.Thread(target=task, daemon=True).start()
