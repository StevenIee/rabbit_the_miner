#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last edited on May 07
Created on Wed Apr 12 00:12:53 2023

@author: Steven Lee
"""
import numpy as np



class DataInfo():
    def __init__(self, player_id):
        # subject information
        self.player_id = player_id;
        self.folder_path = None;
        self.session_num = 0;
        self.stagenum = 0;
        self.group_cond = 1;
        self.session_date = [None, None, None, None, None, None];
        self.restEver = [False,False,False,False,False,False];
        self.save_path = None;
        self.eeg_path = None;
        
        # subject data 
        self.baseline_FAA = [[None, None],[None, None],[None, None],[None, None],[None, None],[None, None]]; # mean, std
        self.base_FAA_result =[None, None, None, None, None, None];
        self.NF_FAA_mean = [[None, None, None, None, None],
                            [None, None, None, None, None],
                            [None, None, None, None, None],
                            [None, None, None, None, None],
                            [None, None, None, None, None],
                            [None, None, None, None, None]];
        self.NF_FAA_result = [[None, None, None, None, None],
                            [None, None, None, None, None],
                            [None, None, None, None, None],
                            [None, None, None, None, None],
                            [None, None, None, None, None],
                            [None, None, None, None, None]];
        self.stage_result = [[[None, None], [None, None], [None, None], [None, None], [None, None]],
                             [[None, None], [None, None], [None, None], [None, None], [None, None]],
                             [[None, None], [None, None], [None, None], [None, None], [None, None]],
                             [[None, None], [None, None], [None, None], [None, None], [None, None]],
                             [[None, None], [None, None], [None, None], [None, None], [None, None]],
                             [[None, None], [None, None], [None, None], [None, None], [None, None]]];
        self.stage_bounds = [[None, None, None, None, None],
                            [None, None, None, None, None],
                            [None, None, None, None, None],
                            [None, None, None, None, None],
                            [None, None, None, None, None],
                            [None, None, None, None, None]];
                             
        
        # EEG data path
        self.EEG_path_baseline = [None, None, None, None, None, None];
        self.EEG_path_game = [[None, None, None, None, None],
                            [None, None, None, None, None],
                            [None, None, None, None, None],
                            [None, None, None, None, None],
                            [None, None, None, None, None],
                            [None, None, None, None, None]];
        