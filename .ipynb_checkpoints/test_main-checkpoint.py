# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 14:08:10 2023

@author: JISU
"""


# import pygame
# import Neurofeedback as NF
from Neurofeedback import Neurofeedback
import GameProcess as GP

# import pygame


if __name__ == "__main__":
    #%% get player data

    player_id, player_session, player_block, player_datafile = GP.player_data()
    
    #%% start game!
    NF = Neurofeedback(player_id, player_session, player_block, player_datafile)