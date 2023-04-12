#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 00:12:53 2023

@author: Steven Lee
"""
import numpy as np



class DataInfo():
    def __init__(self, player_id, session_num):
        self.player_id = player_id;
        self.session_num = session_num;
        self.stagenum = 1;
        self.baseline_FAA = [None, None]; # mean, std
        self.baseline_FAA_fname = None;
        self.restEver = False;
        self.save_path = None;
        self.NF_FAA_mean = [None, None, None, None, None];
        self.NF_FAA_fname = [None, None, None, None, None];
        self.stage_result = [[None, None, None, None, None],[None, None, None, None, None]]