# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 16:07:32 2023

@author: JISU
"""

# import pygame
# from assets import *
import assets as AS
import numpy as np
from datetime import datetime
import time
import EEG_Calc as EC
import TIME_CON as T
import pygame
import os, random
# class Player_data:

# global ani_start
    
def player_data():
  org_path = './'
  # os.chdir(org_path) 
  data_path = org_path + '/data'
  
  if not os.path.isdir(data_path):
    os.mkdir(data_path)

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
  
  return player_id, session_num, player_filename 


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
    connection_check = True
    if button_jstart.draw(screen): 
        game_status_old = game_status
        game_status = "rest_start"
        connection_check = False
    return game_status, game_status_old, connection_check


def resting(screen, game_status, game_status_old, de_x, de_y, resting_back, rest_ins, all_sprites, button_jstart, resting_start, eye_1, mt, base_result, rpy, times, faa_mean, faa_std, resting_num):# resting_eye):
    screen.blit(resting_back,(0,0))
    screen.blit(rest_ins,((de_x-1600)/2,50))
    
    if resting_start:
        cumtime = times[0]; curtime = times[1];
        temp_curtime = time.time();
        cumtime += temp_curtime - curtime;
        curtime = temp_curtime;
        times = [cumtime, curtime];
        if cumtime < T.RESTING_EYE*(1+resting_num):

            AS.resting_eye_play(screen, all_sprites, mt) #* 여기에 알아서 3초 뒤에 시작
            
        elif cumtime < (T.RESTING_EYE + T.RESTING)*(1+resting_num):
            # resting 돌아가고
            # baseline FAA calculator
            temp_buffer = np.array(rpy.root.data_storage);
            time_temp = temp_buffer[4,-int(EC.fft_win_len/2)];
            # online-processing 1. epoching with the newest data
            eeg_temp = temp_buffer[:2,-EC.fft_win_len:];
            
            # online-processing 2. preprocessing
            eeg_rejected = EC.preprocessing(eeg_temp, EC.filter_range, EC.noise_thr,EC.srate)
            
            # calculate data using fft
            faa = EC.calc_asymmetry(eeg_rejected, EC.fft_win_len, EC.cutOff, EC.alpha_idx_range);
            
            base_result.append([faa, cumtime, time_temp])
            # print(faa)
        else:
            # 결과 페이지 나오게 #@JISU 여기 좀 부탁
            faa_mean = np.mean(np.array(base_result)[:,0]);
            faa_std = np.std(np.array(base_result)[:,0]);
            base_result
            if button_jstart.draw(screen): 
                resting_num = resting_num + 1
                game_status_old = game_status
                game_status = "rest_result"
                
                print(faa_mean, faa_std)
        
    else:
        screen.blit(eye_1,(de_x/2-800,de_y/2-220))
        if button_jstart.draw(screen): 
            resting_start = True
            cumtime = 0; curtime = time.time();
            times = [cumtime, curtime];
   
    return game_status, game_status_old, resting_start, base_result, times, faa_mean, faa_std, resting_num


def rest_result(screen, game_status, game_status_old, de_x, de_y, resting_back, rest_rep, base_result, button_start3, button_rerest, faa_mean, faa_std, resting_num):
    screen.blit(resting_back,(0,0))
    screen.blit(rest_rep,((de_x-1000)/2,70))
    
    mean_word = 'Mean : ' + str(round(faa_mean, 2))
    std_word ='Std : ' + str(round(faa_std, 2))
    
    font6 = pygame.font.SysFont('arial',100, True)
    for_mean = font6.render(mean_word, False, 'White')
    for_std = font6.render(std_word, False, 'White')
    mean_x, mean_y = for_mean.get_size()
    std_x, std_y = for_std.get_size()
    
    screen.blit(for_mean, ((de_x-mean_x)/2, 500-(mean_y/1.5)))
    screen.blit(for_std, ((de_x-std_x)/2, 500+(std_y/1.5)))
    
    if button_start3.draw(screen):
        game_status_old = game_status
        game_status = "game_start"
        
    if button_rerest.draw(screen):
        game_status_old = game_status
        game_status = "rest_method"
        # game_rest_did
        
    return game_status, game_status_old




def gaming(screen, game_status, game_status_old, de_x, de_y, faa_mean, faa_std, game_back, game_rd, game_st, game_stop, game_pauseb, pause_title, button_resume, button_main, button_restart, times, nf_result, rpy, game_stat, game_stbar, cart_group, miner_set, game_rock, game_reward, mt, miner_sprites, ani_start):
# def gaming(screen, game_status, game_status_old, de_x, de_y, faa_mean, faa_std, game_back, game_rd, game_st, game_stop, game_pauseb, pause_title, button_resume, button_main, button_restart, times, nf_result, rpy, game_stat, game_stbar, cart_group, miner_set, game_rock, game_reward, mt):
    # background 
    # global ani_start
    screen.blit(game_back,(0,0))
    if game_rd:
        # ready start 화면 2초씩
        # ready
        # screen.blit(game_back,(0,0))
        
        # start
        game_rd = False
        game_st = True
        # time init
        reward_num = 0 # REWARD 누적 된 거 
        
        cumtime = 0; 
        curtime = time.time();
        times = [cumtime , curtime];
        ani_start = False
        
    if game_st:
        temp_curtime = time.time();
        
        if game_stop:
            # game stop 이라면
            screen.blit(game_pauseb,(de_x*0.025,de_y*0.05))
            screen.blit(pause_title,(de_x*0.5-275, de_y*0.2))
            if button_resume.draw(screen):
                game_stop = False               
            if button_main.draw(screen):
                game_status = "intro"
            if button_restart.draw(screen):
                game_status = "game_starting"
        
        else: # game stop이 아니라면
            if times[1] - temp_curtime <= T.NF_update_t: # time update 
                
                # baseline faa
                faa_mean; faa_std;
                # NF faa calc
                temp_buffer = np.array(rpy.root.data_storage);
                time_temp = temp_buffer[4,-int(EC.fft_win_len/2)];
                # online-processing 1. epoching with the newest data
                eeg_temp = temp_buffer[:2,-EC.fft_win_len:];
                # online-processing 2. preprocessing
                eeg_rejected = EC.preprocessing(eeg_temp, EC.filter_range, EC.noise_thr,EC.srate)
                # calculate data using fft
                raw_faa = EC.calc_asymmetry(eeg_rejected, EC.fft_win_len, EC.cutOff, EC.alpha_idx_range);
                faa_z = (raw_faa - faa_mean) /faa_std; # z-score the raw faa by baseline faa
                game_faa, game_bound, statbar_loc = game_faa_convert(faa_z, de_x, de_y)
                
                # time save
                cumtime = times[0];
                curtime = times[1];
                cumtime += temp_curtime - curtime;
                curtime = temp_curtime;
                times = [cumtime, curtime];
                print(curtime)
                
                # stat_barcolor, miner, rock, cart, reward
                screen.blit(game_stat[game_bound],(de_x*0.5-297.5, 50))
                screen.blit(game_stbar, statbar_loc)
                
                # reward 몇개 얻었는지 계산.. 이건 나중에하자! 일단 밑에 카트는 다 half로
                cart_num = 0
                
                
                if game_bound == 0:
                    # rock
                    screen.blit(game_rock,(de_x-600, de_y-600))
                    # miner
                    screen.blit(miner_set[game_bound],(de_x/2-400, de_y-875))
                    # cart
                    screen.blit(cart_group[cart_num],(de_x/2-950, de_y-625))
                    
                
                elif game_bound == 1:
                    # rock
                    screen.blit(game_rock,(de_x-600, de_y-600))
                    # miner
                    screen.blit(miner_set[game_bound],(de_x/2-340, de_y-850))
                    # cart
                    screen.blit(cart_group[cart_num],(de_x/2-950, de_y-625))
                
                elif game_bound == 2:
                    # rock
                    screen.blit(game_rock,(de_x-600, de_y-600))
                    # miner
                    screen.blit(miner_set[game_bound],(de_x/2-400, de_y-875))
                    # cart
                    screen.blit(cart_group[cart_num],(de_x/2-950, de_y-625))
                    
                
                
                else:
                    # reward_select = 1 # 1 gold 2 dia
                    ani_start = True
                    ani_frame = 0
                    
                reward_select = 1 #                    
                # reward_add = 0
                # ani_start = True
                if reward_select == 1:
                    draw_reward = game_reward[0]
                    # draw_reward = pygame.transform.rotate(draw_reward, random.randint(1,4)*90)
                    # reward_select = 0
                elif reward_select == 2:
                    draw_reward = game_reward[1]
                    # draw_reward = pygame.transform.rotate(draw_reward, random.randint(1,4)*90)
                    # reward_select = 0
            
                draw_reward = pygame.transform.rotate(draw_reward, random.randint(1,4)*90)
                
                if ani_start == True:
                    ani_start, ani_frame = AS.miner_ani_starter(screen, miner_sprites, game_bound, mt, game_rock, de_x, de_y, draw_reward, cart_group, cart_num, ani_frame)
                    
                
                # data save
                nf_result.append([raw_faa, cumtime, time_temp])
                
            # game_animation(game_bound)
            if times[0] > T.NF_T:
                #game stop
                game_stop = True;
            
    
    
    return game_status, game_status_old, game_result, game_rd, game_st, game_stop, times, nf_result, ani_start


# def gaming_animations():
    

# def gaming2(screen, game_status, game_status_old, de_x, de_y, faa_mean, faa_std, game_back, game_rd, game_st, game_stop, game_pauseb, pause_title, button_resume, button_main, button_restart, times, nf_result, rpy, game_stat, game_stbar):
#     # background 
#     screen.blit(game_back,(0,0))
#     if game_rd:
#         # ready start 화면 2초씩
#         # ready
#         # screen.blit(game_back,(0,0))
        
#         # start
#         game_rd = False
#         game_st = True
#         # time init

#         cumtime = 0; 
#         curtime = time.time();
#         times = [cumtime , curtime];
        
        
#     if game_st:
#         temp_curtime = time.time();
        
#         if game_stop:
#             # game stop 이라면
#             screen.blit(game_pauseb,(de_x*0.025,de_y*0.05))
#             screen.blit(pause_title,(de_x*0.5-275, de_y*0.2))
#             if button_resume.draw(screen):
#                 game_stop = False               
#             if button_main.draw(screen):
#                 game_status = "intro"
#             if button_restart.draw(screen):
#                 game_status = "game_starting"
        
#         else: # game stop이 아니라면
#             if times[1] - temp_curtime >= T.NF_update_t: # time update 
                
#                 # baseline faa
#                 faa_mean; faa_std;
#                 # NF faa calc
#                 temp_buffer = np.array(rpy.root.data_storage);
#                 time_temp = temp_buffer[4,-int(EC.fft_win_len/2)];
#                 # online-processing 1. epoching with the newest data
#                 eeg_temp = temp_buffer[:2,-EC.fft_win_len:];
#                 # online-processing 2. preprocessing
#                 eeg_rejected = EC.preprocessing(eeg_temp, EC.filter_range, EC.noise_thr,EC.srate)
#                 # calculate data using fft
#                 raw_faa = EC.calc_asymmetry(eeg_rejected, EC.fft_win_len, EC.cutOff, EC.alpha_idx_range);
#                 faa_z = (raw_faa - faa_mean) /faa_std; # z-score the raw faa by baseline faa
#                 game_faa, game_bound, statbar_loc = game_faa_convert(faa_z, de_x, de_y)
                
#                 # time save
#                 cumtime = times[0];
#                 cumtime += temp_curtime - curtime;
#                 curtime = temp_curtime;
#                 times = [cumtime, curtime];
                
                
#                 # stat_barcolor, miner, rock, cart, reward
#                 screen.blit(game_stat[game_bound],(de_x*0.5-297.5, 50))
#                 screen.blit(game_stbar, statbar_loc)

                
#                 # data save
#                 nf_result.append([raw_faa, cumtime, time_temp])
                
#             # game_animation(game_bound)
#             if times[0] > T.NF_T:
#                 #game stop
#                 game_stop = True;
            
    
    
#     return game_status, game_status_old, game_result, game_rd, game_st, game_stop, times, nf_result





def game_faa_convert(faa_z, de_x, de_y):
    #game_faa_range = [-1, 1]
    #game_unit = game_faa_range/5
    #bound_range = [game_unit*(-5), game_unit*(-3), game_unit*(-1), game_unit*(1), game_unit*(3), game_unit*(5)]

    max_faa_std = T.max_faa_std; # = 2
    game_unit = np.linspace((-1)*max_faa_std, max_faa_std, T.faa_steps); # [-2 -1.2 -0.4 0.4 1.2 2];
    bound_range = list(game_unit);
    
    if faa_z > max_faa_std:
        game_faa = max_faa_std
        statbar_loc = (de_x*0.5-297.5-15+(595*.9), 50-7.5)
    
    elif faa_z < (-1)*max_faa_std:
        game_faa = (-1)*max_faa_std
        statbar_loc = (de_x*0.5-297.5-15+(595*.1), 50-7.5)
    
    else:
        game_faa = faa_z
        statbar_loc = (de_x*0.5-297.5-15+(595*(0.5+0.2*game_faa)), 50-7.5) # range에 따라 계속 다시 계산해야 지금은 -2 ~ 2 기준
    
    
    if game_faa >= bound_range[0] and game_faa < bound_range[1]:
        game_bound = 0
    
    elif game_faa >= bound_range[1] and game_faa < bound_range[2]:
        game_bound = 1
    
    elif game_faa >= bound_range[2] and game_faa < bound_range[3]:
        game_bound = 2
        
    elif game_faa >= bound_range[3] and game_faa < bound_range[4]:
        game_bound = 3
        
    elif game_faa >= bound_range[4] and game_faa <= bound_range[5]:
        game_bound = 4
    
    
    return game_faa, game_bound, statbar_loc



def game_result(screen, game_status, game_status_old, game_result, de_x, de_y, game_back, game_cl_b, game_cl_res, cart_result, miner_intro, game_clear, button_main2, button_restart2):
    
    screen.blit(game_back,(0,0))
    screen.blit(game_cl_b,(de_x*0.025,de_y*0.05))
    screen.blit(game_cl_res,(de_x*0.025,de_y*0.5-200))
    screen.blit(cart_result,(de_x-930, de_y-750))
    screen.blit(miner_intro,(de_x-750, de_y-900))
    
    screen.blit(game_clear,(de_x*0.05, 120))
    
    if button_main2.draw(screen):
        game_status_old = game_status
        game_status = "intro"
    if button_restart2.draw(screen):
        game_status_old = game_status
        game_status = "game_starting"
    
    return game_status, game_status_old




