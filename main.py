# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 16:06:44 2023

@author: JISU
"""

# import pygame
# import Neurofeedback as NF
from Neurofeedback import Neurofeedback
import GameProcess as GP

# import pygame

# Some variables for GP.player_data
player_data_is_good = False

if __name__ == "__main__":
    # %% get player data
    
    version_name = '2023.04.03 demo version'
    print1 = '================================================================='
    print(print1)
    print(print1 + '\n')
    print('                      leelab Neurofeedback\n')
    print('                                          '+version_name +'\n')
    print('developed by Steven Lee, Jisu Chung, Minwoo Kim\n')
    print(print1+ '\n\n')
    print('Player Information')
    
    while player_data_is_good is False:
        datainfo, player_datafile, player_data_is_good, tests = GP.player_data(player_data_is_good)


    # %% start game!
    test_mode = True
    # test_mode = False

    datainfo.save_path = player_datafile;

    NF = Neurofeedback(datainfo, test_mode)

    print("ending NF game")

