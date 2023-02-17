# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 16:06:44 2023

@author: JISU
"""


import Neurofeedback as NF
# import pygame



#%% get player data

player_id, player_session, player_datafile = NF.Neurofeedback.player_data()


#%% start game!
# screen_size = (1920,1080)
NF.Neurofeedback.game_init()
