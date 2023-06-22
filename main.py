# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 16:06:44 2023

@author: JISU
"""

# import pygame
# import Neurofeedback as NF
from Neurofeedback import Neurofeedback
import GameProcess_org as GP

# import pygame

# Some variables for GP.player_data
player_data_is_good = False
tests = [0, 0, 0, 0, 0, 0, 0]

if __name__ == "__main__":
    # %% get player data
    

    while player_data_is_good is False:
        player_id, player_session, player_block, manual_faa_mean, manual_faa_std, player_datafile, \
            player_data_is_good, tests = GP.player_data(player_data_is_good, tests)

    # %% start game!
    test_mode = True
    # test_mode = False
    NF = Neurofeedback(player_id, player_session, player_block, manual_faa_mean, manual_faa_std, player_datafile, test_mode)

    print("ending NF game")
