# -*- coding: utf-8 -*-
import customtkinter
from frames.cEMDFrame import cEMDFrame
from frames.stitchFrame import stitchFrame

class MainTabs(customtkinter.CTkTabview):
    def __init__(self, master):
        super().__init__(master)
        
        # Main tabs
        self.cEMD = self.add('Convert EMD')
        self.stitch = self.add('Stitch')
        self.cTrakEM2 = self.add('Convert TrakEM2')
        self._segmented_button.grid(sticky="ew")
        
        #Nested Tab: Convert EMD
        self.cEMDFrame = cEMDFrame(self.cEMD)
        self.cEMDFrame.pack(fill = 'both', expand = 'true')

        self.stitchFrame = stitchFrame(self.stitch)
        self.stitchFrame.pack(fill = 'both', expand = 'true')