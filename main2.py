# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 16:06:44 2023

@author: JISU
"""


from Neurofeedback import Neurofeedback
import GameProcess as GP


valid_inputs = False
tests = [0, 0, 0, 0, 0, 0, 0]

if __name__ == "__main__":
    # get player data

    

    while not valid_inputs:
        valid_inputs = GP.validate_inputs()
    

    # %% start game!
    test_mode = True
    # test_mode = False
    NF = Neurofeedback(player_id, player_session, player_block, manual_faa_mean, manual_faa_std, player_datafile, test_mode)

    print("ending NF game")

