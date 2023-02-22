# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 16:07:32 2023

@author: JISU
"""

# import pygame
# from assets import *
import assets as AS
from datetime import datetime
# class Player_data:
    
def player_data():
  org_path = 'D:/DCNL/DTx/neurofeedback/work'
  # os.chdir(org_path) 
  data_path = org_path + '/data'
  
  
  version_name = '2023.02.20 demo version'
  print1 = '================================================================='
  print(print1)
  print(print1 + '\n')
  
  print('                      leelab Neurofeedback\n')
  
  print('                                          '+version_name +'\n')
  print('developed by Steven Lee, Jisu Chung\n')
  
  print(print1+ '\n\n')
  
  print('Player Information')
  player_id = input('input your id : ')
  session_numi = input('input session number : ')
  session_num = int(session_numi)
  
  player_date_temp = datetime.now()
  player_date = player_date_temp.strftime('%Y_%m_%d_%H%M%S')
  
  player_filename = 'Player_' + player_id + '_Session_' + session_numi + '_' + player_date
  
  
  if session_num > 1:
      print('\n\nWelcome Back!')
  
  
  print('\nloading....\n')    
  
  datafile_name = data_path+'/'+player_filename+'.csv'
  
  
  
  return player_id, session_num, datafile_name
   

def buttons(de_x, de_y, button_starti, button_methodi, button_reresti, button_restarti, button_resumei, button_jstarti, button_maini, button_pausei, button_testi):
    button_start = AS.Button(1400, 700, button_starti, 370, 120)
    button_start2 = AS.Button(de_x/2-165,900, button_starti, 370, 120)
    button_start3 = AS.Button(de_x/2-(165*3),900, button_starti, 370, 120)
    button_method = AS.Button(1400, 840, button_methodi, 370, 120)
    button_rerest = AS.Button(de_x/2+165,900, button_reresti, 370, 120)
    button_restart = AS.Button(de_x*0.5-185, de_y*0.64, button_restarti, 370, 120)
    button_restart2 = AS.Button(580,830, button_restarti, 370, 120)
    button_resume = AS.Button(de_x*0.5-185, de_y*0.77, button_resumei, 370, 120)
    button_jstart = AS.Button(de_x/2-165,900, button_jstarti, 370, 120)
    button_main = AS.Button(de_x*0.5-185, de_y*0.51, button_maini, 370, 120)
    button_main2 = AS.Button(130,830, button_maini, 370, 120)
    button_pause = AS.Button(de_x*0.94, 40, button_pausei, 70, 70)
    
    
    button_right = AS.Button(de_x*0.94, de_y-200, button_pausei, 70, 70)
    
    button_left = AS.Button(de_x*0.94-100, de_y-200, button_pausei, 70, 70)
    button_up = AS.Button(de_x*0.94-50, de_y-250, button_pausei, 70, 70)
    button_down = AS.Button(de_x*0.94-50, de_y-150, button_pausei, 70, 70)
    button_test = AS.Button(de_x*0.94, de_y-350, button_testi, 70, 70)
    
    return button_start, button_start2, button_start3, button_method, button_rerest, button_restart, button_restart2, button_resume, button_jstart, button_main, button_main2, button_pause, button_right, button_left, button_up, button_down, button_test


def intro(screen, background_img, title_gold, title_word, miner_intro, cart_full, button_method, button_start, game_status, game_status_old):        
    screen.blit(background_img,(0,0))
    screen.blit(title_gold,(1050,40))
    screen.blit(title_word,(1200,50))
    screen.blit(miner_intro,(140,250))
    screen.blit(cart_full,(750,450))
    if button_method.draw(screen):
        game_status_old = game_status
        game_status = "method"
    if button_start.draw(screen):
        game_status_old = game_status
        game_status = "rest_method"
    
    return game_status, game_status_old

def method(screen, game_status, game_status_old, de_x, de_y, method_back, button_start2, method):
    screen.blit(method_back,(0,0))
    screen.blit(method,((de_x-1400)/2,100))
    if button_start2.draw(screen):
        game_status_old = game_status
        game_status = "rest_method"
        
    return game_status, game_status_old

    
def rest_method(screen, game_status, game_status_old, de_x, de_y, resting_back, rest_expl, rest_title, button_jstart):
    screen.blit(resting_back,(0,0))    
    screen.blit(rest_expl,(de_x*0.05,de_y*0.07))
    screen.blit(rest_title,((de_x-1000)/2,50))
    if button_jstart.draw(screen): 
        game_status_old = game_status
        game_status = "rest_start"
                
    return game_status, game_status_old


def resting(screen, game_status, game_status_old, de_x, de_y, resting_back, rest_ins, all_sprites, button_jstart, resting_start, eye_1, mt):# resting_eye):
    screen.blit(resting_back,(0,0))
    screen.blit(rest_ins,((de_x-1600)/2,50))
    # screen.blit(resting_eye,(de_x/2-800,de_y/2-220))
    # resting_eye()
    # resting_eye = AS.resting_eye((de_x/2-800,de_y/2-220))
    # resting_eye.update()
    # all_sprites
    # all_sprites.draw(screen)
    
    if resting_start:
        AS.resting_eye_play(screen, all_sprites, mt)
    else:
        screen.blit(eye_1,(de_x/2-800,de_y/2-220))
        if button_jstart.draw(screen): 
            resting_start = True
    
    return game_status, game_status_old, resting_start



#     return game_status



# def gaming(screen, game_status):
    
#     return game_status

