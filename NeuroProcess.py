# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 16:07:17 2023

@author: JISU
"""

from datetime import date
from NF_laxtha_v2 import NNFX2_FAA

class Baseline:
    
    def __init__(self, player_id, player_session, player_datafile):
        
        Base = NNFX2_FAA(player_datafile)
        Base.set_EEGcalc(5, 0.1);
        self.faa_all = Base.baseline_recording(180, 1000, [8, 13]) # <- duration set



    def 