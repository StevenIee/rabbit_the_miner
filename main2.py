# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 16:06:44 2023

@author: JISU
"""


from Neurofeedback import Neurofeedback
import GameProcess_org as GP


valid_inputs = False
default_values = ["999", "999", "1", "0", "0"]
tests = [0, 0, 0, 0, 0, 0, 0]

if __name__ == "__main__":
    # get player data
    game_process = GP.PlayerInfoForm(default_values, tests)  # Create an instance of the PlayerInfoForm class
    valid_inputs = False
    
    while not valid_inputs:
        player_info = game_process.validate_inputs(default_values, tests)
        if player_info is not None:
            player_id, player_session, player_block, manual_faa_mean, manual_faa_std, player_datafile = player_info
            valid_inputs = True
    

    # %% start game!
    test_mode = True
    # test_mode = False
    NF = Neurofeedback(player_id, player_session, player_block, manual_faa_mean, manual_faa_std, player_datafile, test_mode)

    print("ending NF game")


 