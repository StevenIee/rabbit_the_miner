'''

Organized version of GameProcess.py

@ 2023.06.15

@ jeonghwan7191@gmail.com

'''

import assets as AS
import numpy as np
from datetime import datetime
import time
import EEG_Calc as EC
import TIME_CON as T
import pygame
import os
import random
import sys
import tkinter as tk
from tkinter import messagebox

#Global Variables
root = None
org_path = './'
data_path = None

# Helper functions
def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    
def create_gui():
    global root
    root = tk.Tk()
    root.geometry('500x450')
    root.eval('tk::PlaceWindow . center')
    root.title("참여자 정보")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
def on_closing():
    sys.exit()

#Getting player info and saving into a file
class PlayerInfoForm(tk.Tk):
    def __init__(self, default_values, tests):
        super().__init__()

        self.default_values = ["999", "999", "1", "0", "0"]
        
        self.player_id = tk.StringVar()
        self.session_num = tk.StringVar()
        self.stage_num = tk.StringVar()
        self.manual_faa_mean = tk.StringVar()
        self.manual_faa_std = tk.StringVar()

        
        self.tests = tests
        
        self.create_widgets()
        #create_gui()
        
    def create_widgets(self):
        
        tests = [0, 0, 0, 0, 0, 0] 
        
        player_id_default_text = "type integer" if not tests[0] else "999"
        session_default_text = "type integer" if not tests[1] else "999"
        stage_num_default_text = "type integers 1 to 5" if not tests[2] or not tests[5] else "1"
        manual_mfm_default_text = "enter faa mean in float" if not tests[3] else "0"
        manual_mfs_default_text = "enter faa std in float" if not tests[4] else "0"
        if not tests[6]:
            stage_num_default_text = "faa is 0 for stage 1"
            manual_mfs_default_text = "0"
            manual_mfm_default_text = "0"
        
        
        tk.Label(root, text="참여자 정보", width=20, font=("bold", 20)).place(x=90, y=53)
        
        tk.Label(root, text="피험자번호", width=20, font=("bold", 10)).place(x=68, y=130)
        tk.Entry(root, textvariable=self.player_id).place(x=240, y=130)

        tk.Label(root, text="세션번호", width=20, font=("bold", 10)).place(x=68, y=180)
        tk.Entry(root, textvariable=self.session_num).place(x=240, y=180)

        tk.Label(root, text="블록번호", width=20, font=("bold", 10)).place(x=68, y=230)
        tk.Entry(root, textvariable=self.stage_num).place(x=240, y=230)

        tk.Label(root, text="휴지기 FAA 평균", width=20, font=("bold", 10)).place(x=68, y=280)
        tk.Entry(root, textvariable=self.manual_faa_mean).place(x=240, y=280)

        tk.Label(root, text="휴지기 FAA std", width=20, font=("bold", 10)).place(x=68, y=320)
        tk.Entry(root, textvariable=self.manual_faa_std).place(x=240, y=320)

        tk.Button(root, text='입력완료', width=20, bg='brown', fg='white', command=self.submit_player_info).place(x=180, y=360)
        
        self.player_id.set(player_id_default_text)
        self.session_num.set(session_default_text)
        self.stage_num.set(stage_num_default_text)
        self.manual_faa_mean.set(manual_mfm_default_text)
        self.manual_faa_std.set(manual_mfs_default_text)

        
    def validate_inputs(self, default_values, tests, player_datafile):
        
        player_id = self.player_id.get()
        session_num = self.session_num.get()
        stage_num = self.stage_num.get()
        manual_faa_mean = self.manual_faa_mean.get()
        manual_faa_std = self.manual_faa_std.get()

        if not is_number(player_id):
            return None
        if not is_number(session_num):
            return None
        if not is_number(stage_num):
            return None
        if not is_number(manual_faa_mean):
            return None
        if not is_number(manual_faa_std):
            return None

        stage_num = int(stage_num)

        if stage_num < 1 or stage_num > 5:
            return None
        elif stage_num != 1 and (float(manual_faa_mean) == 0 or float(manual_faa_std) == 0):
            return None
        
        return player_id, session_num, stage_num, manual_faa_mean, manual_faa_std, player_datafile, tests

    def print_player_info(self):
        player_id = self.player_id.get()
        session_num = self.session_num.get()
        stage_num = self.stage_num.get()
        manual_faa_mean = self.manual_faa_mean.get()
        manual_faa_std = self.manual_faa_std.get()
        
        print("Player_Id: ", player_id)
        print("Session_#: ", session_num)
        print("Block___#: ", stage_num)
        print("manual_faa_mean: ", manual_faa_mean)
        print("manual_faa_std: ", manual_faa_std)
    
    def submit_player_info(self):
        validation_result = self.validate_inputs()
        if validation_result is not None:
            self.print_player_info()
            if root is not None and root.winfo_exists():
                self.destroy()
        else:
            messagebox.showerror("Invalid Input", "Please enter valid player information.")

    def save_player_data(self):
        player_id = self.player_id.get()
        session_num = self.session_num.get()
        stage_num = self.stage_num.get()
        manual_faa_mean = self.manual_faa_mean.get()
        manual_faa_std = self.manual_faa_std.get()

        self.print_player_info()
    
        player_date_temp = datetime.now()
        player_date = player_date_temp.strftime('%Y_%m_%d_%H%M%S')

        player_filename = 'Player_' + str(player_id) + '_Session_' + str(session_num) + '_' + player_date

        if session_num > 1:
            print('\n\nWelcome Back!')

        print('\nloading....\n')

        datafile_name = data_path + '/' + player_filename + '.csv'
    

        return player_filename

    #class ends
    
#Receiving player data and save.
#Game loop
def player_data(default_values, tests):
    global root, data_path
    
    create_gui()
    
    data_path = org_path + '/data'
    
    if not os.path.isdir(data_path):
        os.mkdir(data_path)
        
    version_name = '2023.04.03 demo version'
    print1 = '================================================================='
    print(print1)
    print(print1 + '\n')
    print('                      leelab Neurofeedback\n')
    print('                                          '+version_name +'\n')
    print('developed by Steven Lee, Jisu Chung, Minwoo Kim\n')
    print(print1+ '\n\n')
    print('Player Information')

    player_info_form = PlayerInfoForm(default_values, tests)
    root.mainloop()
    
#  Create Buttons for the Game
#  Grouped the buttons logically based on their purpose or location. 
def create_start_buttons(de_x, de_y, button_starti):
    button_start = AS.Button(1400, 770, button_starti, 370, 120)
    button_start2 = AS.Button(de_x / 2 - 165, 900, button_starti, 370, 120)
    button_start3 = AS.Button(de_x / 2 - (165 * 3), 900, button_starti, 370, 120)
    return button_start, button_start2, button_start3

def create_navigation_buttons(de_x, de_y, button_pausei, button_maini, button_restarti, button_resumei, button_jstarti, button_reresti, button_methodi):
    button_restart = AS.Button(de_x * 0.5 - 185, de_y * 0.64, button_restarti, 370, 120)
    button_restart2 = AS.Button(580, 830, button_resumei, 370, 120)
    button_resume = AS.Button(de_x * 0.5 - 185, de_y * 0.77, button_resumei, 370, 120)
    button_jstart = AS.Button(de_x / 2 - 165, 900, button_jstarti, 370, 120)
    button_main = AS.Button(de_x * 0.5 - 185, de_y * 0.51, button_maini, 370, 120)
    button_main2 = AS.Button(130, 830, button_maini, 370, 120)
    button_pause = AS.Button(de_x * 0.94, 40, button_pausei, 70, 70)
    button_rerest = AS.Button(de_x/2+165,900, button_reresti, 370, 120)
    button_method = AS.Button(1400, 840, button_methodi, 370, 120)
    return button_restart, button_restart2, button_resume, button_jstart, button_main, button_main2, button_pause, button_rerest, button_method

def create_direction_buttons(de_x, de_y, button_pausei):
    button_right = AS.Button(de_x * 0.94, de_y - 200, button_pausei, 70, 70)
    button_left = AS.Button(de_x * 0.94 - 100, de_y - 200, button_pausei, 70, 70)
    button_up = AS.Button(de_x * 0.94 - 50, de_y - 250, button_pausei, 70, 70)
    button_down = AS.Button(de_x * 0.94 - 50, de_y - 150, button_pausei, 70, 70)
    return button_right, button_left, button_up, button_down

def create_test_button(de_x, de_y, button_testi):
    button_test = AS.Button(de_x * 0.94, de_y - 350, button_testi, 70, 70)
    return button_test

def create_buttons(de_x, de_y, button_starti, button_methodi, button_reresti, button_restarti, button_resumei, button_jstarti, button_maini, button_pausei, button_testi):
    start_buttons = create_start_buttons(de_x, de_y, button_starti)
    navigation_buttons = create_navigation_buttons(de_x, de_y, button_pausei)
    direction_buttons = create_direction_buttons(de_x, de_y, button_pausei)
   

#여기서부터 안바꿈 (comment만 날림)

#Intro Class
def intro(screen, background_img, title_gold, title_word, miner_intro, cart_full, button_method, button_start, game_status, game_status_old):
    screen.blit(background_img, (0, 0))
    screen.blit(title_gold, (1100, 70)) # 1050,40
    screen.blit(title_word, (1200, 50))
    screen.blit(miner_intro, (140, 250))
    screen.blit(cart_full, (750, 450))

    if button_start.draw(screen):
        game_status_old = game_status
        game_status = "rest_method"
    
    return game_status, game_status_old


def method(screen, game_status, game_status_old, de_x, de_y, method_back, button_start2, method):
    screen.blit(method_back, (0, 0))
    screen.blit(method, ((de_x-1400)/2, 100))
    if button_start2.draw(screen):
        game_status_old = game_status
        game_status = "game_start"
        
    return game_status, game_status_old


def rest_method(screen, game_status, game_status_old, de_x, de_y, resting_back, rest_expl, rest_title, button_jstart):
    screen.blit(resting_back, (0, 0))
    screen.blit(rest_expl, (de_x*0.05, de_y*0.07))
    screen.blit(rest_title, ((de_x-1000)/2, 50))
    connection_check = True

    # rest start를 유발한하는 버튼.
    if button_jstart.draw(screen): 
        game_status_old = game_status
        game_status = "rest_start"
        connection_check = False
    return game_status, game_status_old, connection_check


def resting(screen, game_status, game_status_old, de_x, de_y, resting_back, rest_ins, all_sprites, button_jstart, resting_start, eye_1, mt, base_result, rpy, times, faa_mean, faa_std, resting_num, test_mode):

    screen.blit(resting_back, (0, 0))
    screen.blit(rest_ins, ((de_x-1600)/2, 50))

    if resting_start is False:
        resting_start = True
        cumtime = 0
        curtime = time.time()

    elif resting_start is True:
        cumtime = times[0]
        curtime = times[1]
        temp_curtime = time.time()
        cumtime += temp_curtime - curtime
        curtime = temp_curtime


    times = [round(cumtime, 3), round(curtime, 3)]

    if cumtime < T.RESTING_EYE:
        AS.resting_eye_play(screen, all_sprites, mt)
        if button_jstart.draw(screen):
            print(faa_mean, faa_std)

    elif cumtime > T.RESTING_EYE and cumtime < (T.RESTING_EYE + T.RESTING):
        
        resting_cumtime = cumtime - T.RESTING_EYE

        # resting 돌아가고
        # baseline FAA calculator
        temp_buffer = np.array(rpy.root.data_storage)

        # print(temp_buffer)
        time_temp = temp_buffer[4, -int(EC.fft_win_len/2)]

        # online-processing 1. epoching with the newest data
        eeg_temp = temp_buffer[:2, -EC.fft_win_len:]

        # online-processing 2. preprocessing
        eeg_rejected = EC.preprocessing(eeg_temp, EC.filter_range, EC.noise_thr, EC.srate)

        # calculate data using fft
        faa = EC.calc_asymmetry(eeg_rejected, EC.fft_win_len, EC.cutOff, EC.alpha_idx_range);

        base_result.append([round(faa, 3), round(cumtime, 3), time_temp])
        # print(faa)
    else:
        faa_mean = np.mean(np.array(base_result)[:, 0])
        faa_std = np.std(np.array(base_result)[:, 0])
        if test_mode:
            faa_mean = -0.7
            faa_std = 0
        
        resting_num = resting_num + 1
        game_status_old = game_status
        # 결과 페이지 상태 설정
        game_status = "rest_result"

    return game_status, game_status_old, resting_start, base_result, faa_mean, faa_std, resting_num


def rest_result(screen, game_status, game_status_old, de_x, de_y, resting_back, rest_rep, base_result, button_start3, button_rerest, faa_mean, faa_std, resting_num):
    screen.blit(resting_back, (0, 0))
    screen.blit(rest_rep, ((de_x-1000)/2, 70))
    
    mean_word = 'Mean : ' + str(round(faa_mean, 2))
    std_word ='Std : ' + str(round(faa_std, 2))
    
    font6 = pygame.font.SysFont('arial', 100, True)
    for_mean = font6.render(mean_word, False, 'White')
    for_std = font6.render(std_word, False, 'White')
    mean_x, mean_y = for_mean.get_size()
    std_x, std_y = for_std.get_size()
    
    screen.blit(for_mean, ((de_x-mean_x)/2, 500-(mean_y/1.5)))
    screen.blit(for_std, ((de_x-std_x)/2, 500+(std_y/1.5)))
    
    if button_start3.draw(screen):
        game_status_old = game_status
        game_status = "method"
        
    if button_rerest.draw(screen):
        game_status_old = game_status
        game_status = "rest_method"
        # game_rest_did
        
    return game_status, game_status_old



def gaming(screen, game_status, game_status_old, de_x, de_y, faa_mean, faa_std, game_back, game_rd, game_st, game_stop,
           game_pauseb, pause_title, button_pause, button_resume, button_main, button_restart, times, nf_result, rpy, game_stat,
           game_stbar, cart_group, miner_set, game_rock, game_reward, mt, miner_sprites, ani_start, ani_frame, test_mode, block_num,
           game_ready, game_bound, game_bound_old, draw_reward, bound_time, index_num, reward_frame, stage_result, reward_num):

    starting_time = 4

    if game_st is False:
        game_st = True

        cumtime = 0
        curtime = time.time()
        times = [[round(cumtime, 3), round(curtime, 3)], [round(cumtime, 3), round(curtime, 3)]];
        print(game_st)
    
       
    elif time.time() - times[0][1] > starting_time:
        cumtime = time.time() - times[0][1]
        curtime = time.time();
        times = [[round(cumtime, 3), round(curtime, 3)], [round(cumtime, 3), round(curtime, 3)]];
    
    screen.blit(game_back, (0, 0))

    if times[0][0] > starting_time and game_st is True:

        if game_stop:
            screen.blit(game_pauseb, (de_x*0.025, de_y*0.05))
            screen.blit(pause_title, (de_x*0.5-275, de_y*0.2))
            if button_resume.draw(screen):
                game_stop = False
            if button_main.draw(screen):
                game_status = "intro"
                game_stop = False
            if button_restart.draw(screen):
                game_status = "game_start"
                game_st = False
                game_stop = False

        else:
            temp_curtime = time.time();
            if times[0][1] - temp_curtime <= T.NF_update_t:  

                faa_mean; faa_std;
                temp_buffer = np.array(rpy.root.data_storage);
                time_temp = temp_buffer[4,-int(EC.fft_win_len/2)];
                eeg_temp = temp_buffer[:2,-EC.fft_win_len:];
                eeg_rejected = EC.preprocessing(eeg_temp, EC.filter_range, EC.noise_thr,EC.srate)
                raw_faa = EC.calc_asymmetry(eeg_rejected, EC.fft_win_len, EC.cutOff, EC.alpha_idx_range);
                faa_z = (raw_faa - faa_mean) /faa_std; 
                game_faa, statbar_loc = statbar_loc_convert(faa_z, de_x, de_y)

                
                # time save
                cumtime = times[0][0];
                curtime = times[0][1];
                cumtime += temp_curtime - curtime;
                curtime = temp_curtime;
                
                times[0][0] = cumtime;
                times[0][1] = curtime;

                # FAA save
                nf_result.append([raw_faa, cumtime, time_temp])


            temp_curtime = time.time();
            if times[1][1] - temp_curtime <= T.anim_update_t:
                n_avgfaa = round(T.anim_update_t / T.NF_update_t);
                
                if len(nf_result) <n_avgfaa:
                    temp_faas = np.array(nf_result)[:, 0] 
                else:
                    temp_faas = np.array(nf_result[-1*n_avgfaa:])[:, 0] 
                avgfaa = np.nanmean(temp_faas)
            
                faa_z = (avgfaa - faa_mean) /faa_std; 
                game_faa, game_bound = game_faa_convert(faa_z, de_x, de_y)
                if test_mode:
                    game_bound = 4

            screen.blit(game_stat[game_bound],(de_x*0.5-297.5, 50))
            screen.blit(game_stbar, statbar_loc)

            cart_num = 0
            
            
            if stage_result[0] + stage_result[1] > 20:
                cart_num = 2
            elif stage_result[0] + stage_result[1] > 10:
                cart_num = 1
            else:
                cart_num = 0
            
            if ani_start:
                
                ani_start, ani_frame, index_num, reward_frame, stage_result = AS.miner_ani_starter(screen, miner_sprites, game_bound, mt, game_rock, de_x, de_y, draw_reward, reward_num, cart_group, cart_num, ani_frame, index_num, reward_frame, stage_result, game_bound)
                
            elif game_bound == 3 or game_bound == 4:
                ani_start = True
                ani_frame = 0
                reward_frame = 0
                
                draw_reward, bound_time, reward_num = miner_animate(game_bound, game_bound_old, temp_curtime, game_reward, draw_reward, bound_time, reward_num)
                screen.blit(game_rock,(de_x-600, de_y-600))
                screen.blit(miner_set[3],(690, 205))
                screen.blit(cart_group[cart_num],(de_x/2-950, de_y-625))

    
            elif game_bound == 0:
                # rock
                screen.blit(game_rock,(de_x-600, de_y-600))
                # miner
                screen.blit(miner_set[game_bound],(690, 205))
                # cart
                screen.blit(cart_group[cart_num],(de_x/2-950, de_y-625))


            elif game_bound == 1:
                # rock
                screen.blit(game_rock,(de_x-600, de_y-600))
                # miner
                screen.blit(miner_set[game_bound], (690, 205))
                # cart
                screen.blit(cart_group[cart_num],(de_x/2-950, de_y-625))

            elif game_bound == 2:
                # rock
                screen.blit(game_rock,(de_x-600, de_y-600))
                # miner
                screen.blit(miner_set[game_bound],(690, 205))
                # cart
                screen.blit(cart_group[cart_num],(de_x/2-950, de_y-625))
            game_bound_old = game_bound
            

            # game_animation(game_bound)
            if times[0][0] > T.NF_T:
                # game stop
                game_stop = True
                game_status = "game_result"
            
            if button_pause.draw(screen):
                game_stop = True    

    elif time.time() - times[0][1] < 2:
        screen.blit(game_pauseb, (de_x*0.025, de_y*0.05))
        block_word = 'Stage ' + str(block_num)
        
        font6 = pygame.font.SysFont('arial', 250, True)
        for_block = font6.render(block_word, False, 'White')
        block_x, block_y = for_block.get_size()
        
        screen.blit(for_block, ((de_x-block_x)/2, (de_y-block_y)/2))
   
    # ready
    else:
        screen.blit(game_rock,(de_x-600, de_y-600))
        # miner
        screen.blit(miner_set[3],(690, 205))
        # cart
        screen.blit(cart_group[0],(de_x/2-950, de_y-625))
        # ready
        screen.blit(game_ready, (de_x/2-900,de_y-800))
        
    

    return game_status, game_status_old, stage_result, game_rd, game_st, game_stop, times, nf_result, ani_start, ani_frame, game_bound, game_bound_old, draw_reward, bound_time, index_num, reward_frame, reward_num 


def miner_animate(game_bound, game_bound_old, temp_curtime, game_reward, draw_reward, bound_time, reward_num):
    
    if game_bound_old < 3 :
        bound_time[0] = temp_curtime
    else:
        bound_time[1] = temp_curtime
        bound_time[2] = bound_time[1] - bound_time[0]
        draw_reward = game_reward[0]
        reward_num = 1
        
        if bound_time[2] >= 10:
            draw_reward = game_reward[1]
            draw_reward = pygame.transform.rotate(draw_reward, random.randint(1,4)*90)
            bound_time[0] = temp_curtime
            reward_num = 2
        elif draw_reward != game_reward[1] and bound_time[2] < 10:
            draw_reward = game_reward[0]
            draw_reward = pygame.transform.rotate(draw_reward, random.randint(1,4)*90)
            reward_num = 1
    return draw_reward, bound_time, reward_num #miner_wait


def statbar_loc_convert(faa_z, de_x, de_y):
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
        statbar_loc = (de_x*0.5-297.5-15+(595*(0.5+0.2*game_faa)), 50-7.5) 
    
    return game_faa, statbar_loc


def game_faa_convert(faa_z, de_x, de_y):
    max_faa_std = T.max_faa_std; # = 2
    game_unit = np.linspace((-1)*max_faa_std, max_faa_std, T.faa_steps); 
    bound_range = list(game_unit);
    
    if faa_z > max_faa_std:
        game_faa = max_faa_std
    
    elif faa_z < (-1)*max_faa_std:
        game_faa = (-1)*max_faa_std
    
    else:
        game_faa = faa_z
    
    game_bound = 0
    
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
    
    
    return game_faa, game_bound 


def game_result(screen, game_status, game_status_old, stage_result, de_x, de_y, game_back, game_cl_b, game_cl_res, cart_result, miner_intro, game_clear, button_main2, button_restart2, block_num):
    
    screen.blit(game_back, (0, 0))
    screen.blit(game_cl_b, (de_x*0.025, de_y*0.05))
    screen.blit(game_cl_res, (de_x*0.025, de_y*0.5-200))
    screen.blit(cart_result, (de_x-930, de_y-750))
    screen.blit(miner_intro, (de_x-750, de_y-900))
    screen.blit(game_clear, (de_x*0.05, 120))
    
    # stage_result 보여주기
        
    gold_word = '  :  ' + str(stage_result[0])
    dia_word ='  :  ' + str(stage_result[1])
    
    font6 = pygame.font.SysFont('arial', 100, True)
    for_gold = font6.render(gold_word, False, 'White')
    for_dia = font6.render(dia_word, False, 'White')
    gold_x, gold_y = for_gold.get_size()
    dia_x, dia_y = for_dia.get_size()
    
    screen.blit(for_gold, ((de_x-500-gold_x)/2, 500-(gold_y/1.3)))
    screen.blit(for_dia, ((de_x-500-dia_x)/2, 500+(dia_y/1.5)))
    
    if button_main2.draw(screen):
        game_status_old = game_status
        game_status = "intro"
    if button_restart2.draw(screen):
        block_num = block_num + 1
        game_status_old = game_status
        game_status = "game_start"
    
    return game_status, game_status_old, block_num

