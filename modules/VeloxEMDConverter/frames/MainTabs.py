# -*- coding: utf-8 -*-
import customtkinter
from .cEMDFrame import cEMDFrame
from .StitchFrame import StitchFrame
from .cTrakEM2Frame import cTrakEM2Frame

class MainTabs(customtkinter.CTkTabview):
    def __init__(self, master):
        super().__init__(master)
        
        # Main tabs
        self.cEMD = self.add('Convert EMD(s)')
        self.stitch = self.add('Stitch mosaic(s)')
        self.cTrakEM2 = self.add('Convert TrakEM2 mosaic(s)')
        self._segmented_button.grid(sticky="ew")
        
        #Nested Tab: Convert EMD
        self.cEMDFrame = cEMDFrame(self.cEMD)
        self.cEMDFrame.pack(fill = 'both', expand = 'true')

        self.StitchFrame = StitchFrame(self.stitch)
        self.StitchFrame.pack(fill = 'both', expand = 'true')

        self.cTrakEM2Frame = cTrakEM2Frame(self.cTrakEM2)
        self.cTrakEM2Frame.pack(fill = 'both', expand = 'true')