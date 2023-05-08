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
import sys
import tkinter as tk
import pickle
from DataInfo import DataInfo

# class Player_data:

# global ani_start
from tkinter import messagebox


def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def player_data(player_info_is_good, tests, ):
    global root
    """
    :param player_info_is_good: False로 놓고 while 구문안에 넣은 뒤 조건을 충족하면 True로 전환하여 loop을 깨는 구조로 사용하면 됨.
    :param tests: 일곱가지 테스트에 대한 list. 처음에는 [0,0,0,0,0,0,0] 혹은 [False, False, False, False, False, False, False]로 설정.
                  이 리스트에 따라 그 다음에 나오는 info창의 문구가 결정된다. 오류가 있는 입력창의 문구가 변환됨.
    :return:
    player_id : 플레이어 식별 변호
    session_num : 몇 번째 방문한 것인지 기록.
    stage_num : 스테이지를 수동으로 입력해야할 때 입력. 기본은 1부터 시작함. 스테이지 2부터 수동 faa값 필요.
    manual_faa_mean : 수동으로 입력하는 FAA 평균값, stage2부터 필요함.
    manual_faa_std : 수동으로 입력하는 FAA 표준편차값, stage2부터 필요함.
    player_filename : 플레이어 파일명
    player_info_is_good : param과 동일
    tests: param의 tests와 동일.
    """

    
    datainfo = None;
    
    root = tk.Tk()
    root.geometry('500x450')
    root.eval('tk::PlaceWindow . center')
    root.title("참여자 정보")
    
    def on_closing():
        sys.exit()

    if tests[0] is False:
        player_id_default_text = "type integer"
    else:
        player_id_default_text = "999"

    if tests[1] is False:
        session_default_text = "type integer"
    else:
        session_default_text = "999"

    if tests[2] is False or tests[5] is False:
        stage_num_default_text = "type integers 1 to 5"
    else:
        stage_num_default_text = "1"

    if tests[3] is False:
        manual_mfm_default_text = "enter faa mean in float"
    else:
        manual_mfm_default_text = "0"

    if tests[4] is False:
        manual_mfs_default_text = "enter faa std in float"
    else:
        manual_mfs_default_text = "0"

    if tests[6] is False:
        stage_num_default_text = "faa is 0 for stage 1"
        manual_mfs_default_text = "0"
        manual_mfm_default_text = "0"
    else:
        pass

    tk.Label(root, text="참여자 정보", width=20, font=("bold", 20)).place(x=90, y=53)

    tk.Label(root, text="피험자번호", width=20, font=("bold", 10)).place(x=68, y=130)
    player_id = tk.StringVar()
    player_id.set(player_id_default_text)
    tk.Entry(root, textvariable=player_id).place(x=240, y=130)

    tk.Label(root, text="세션번호", width=20, font=("bold", 10)).place(x=68, y=180)
    session_num = tk.StringVar()
    session_num.set(session_default_text)
    tk.Entry(root, textvariable=session_num).place(x=240, y=180)

    tk.Label(root, text="블록번호", width=20, font=("bold", 10)).place(x=68, y=230)
    stage_num = tk.StringVar()
    stage_num.set(stage_num_default_text)
    tk.Entry(root, textvariable=stage_num).place(x=240, y=230)

    tk.Label(root, text="휴지기 FAA 평균", width=20, font=("bold", 10)).place(x=68, y=280)
    manual_faa_mean = tk.StringVar()
    manual_faa_mean.set(manual_mfm_default_text)
    tk.Entry(root, textvariable=manual_faa_mean).place(x=240, y=280)

    tk.Label(root, text="휴지기 FAA std", width=20, font=("bold", 10)).place(x=68, y=320)
    manual_faa_std = tk.StringVar()
    manual_faa_std.set(manual_mfs_default_text)
    tk.Entry(root, textvariable=manual_faa_std).place(x=240, y=320)

    tk.Button(root, text='입력완료', width=20, bg='brown', fg='white', command=root.destroy).place(x=180, y=360)

    # root.overrideredirect(True)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # it is use for display the registration form on the window
    root.mainloop()

    # check if the input is all numeric
    check_id = is_number(str(player_id.get()))
    check_session = is_number(str(session_num.get()))
    check_stage = is_number(str(stage_num.get()))
    check_mfm = is_number(str(manual_faa_mean.get()))
    check_mfs = is_number(str(manual_faa_std.get()))

    # check if the stage input is less than or equal to five stages
    stage_less_than_six = False
    stage_faa_check = False

    if check_stage is True:
        if int(stage_num.get()) < 6:
            stage_less_than_six = True
            if int(stage_num.get()) == 1:
                if float(manual_faa_mean.get()) == 0 and float(manual_faa_std.get()) == 0:
                    stage_faa_check = True
                elif float(manual_faa_mean.get()) != 0 or float(manual_faa_std.get()) != 0:
                    stage_faa_check = False
            elif int(stage_num.get()) in [2, 3, 4, 5]:
                stage_faa_check = True
        elif int(stage_num.get()) >= 6:
            stage_less_than_six = False

    tests = [check_id, check_session, check_stage, check_mfm, check_mfs, stage_less_than_six, stage_faa_check]
    # check if all the tests have been good. If good say player_info_is_good is good and move on.
    if all(tests):  # all() tests if list contains False. Returns True when all is True.
        player_info_is_good = True
        
        player_id = int(player_id.get())
        session_num = int(session_num.get())
        stage_num = int(stage_num.get())
        manual_faa_mean = float(manual_faa_mean.get())
        manual_faa_std = float(manual_faa_std.get())

        print("Player_Id: ", player_id)
        print("Session_#: ", session_num)
        print("Block___#: ", stage_num)
        print("manual_faa_mean: ", manual_faa_mean)
        print("manual_faa_std: ", manual_faa_std)

        player_date_temp = datetime.now()
        player_date = player_date_temp.strftime('%Y_%m_%d_%H%M%S')
        
        # data saving path
        org_path = './'
        if not os.path.isdir(org_path+'data/'):
            os.mkdir(org_path+'data/')
            
        data_path = org_path + 'data/' + str(player_id) 
        if not os.path.isdir(data_path):
            os.mkdir(data_path)
            os.mkdir(data_path+'/fig')
            player_filename = 'Player_' + str(player_id) ##
            datafile_name = data_path + '/' + player_filename + '_data.pickle' ##
            
            # init data
            datainfo = DataInfo(player_id);
            datainfo.folder_path = data_path;
            with open(file= datafile_name, mode='wb') as f:
                pickle.dump(datainfo, f)
                
        if not session_num == 1:
            print('\n\nWelcome Back!')
            with open(file=datafile_name, mode='rb') as f:
                datainfo=pickle.load(f)
            if datainfo.session_num == session_num:
                pass
            else:
                print('please check the session number')
                print('last session was ' + str(datainfo.session_num-1))
                print('please put session number ' + str(datainfo.session))
                player_info_is_good = False  
        
        
        if datainfo.stagenum == stage_num: # game_result
            if datainfo.stagenum == 1:
                datainfo.session_date = player_date;
            
        else:
            print('please check the block number')
            print('last block was ' + str(datainfo.stagenum-1))
            print('please put block number ' + str(datainfo.stagenum))
            player_info_is_good = False    
        
        
                


            

        #print('\nloading....\n')
        #print(player_info_is_good)
        
    else:
        player_info_is_good = False
        datafile_name = ""

    #return player_id, session_num, stage_num, manual_faa_mean, manual_faa_std, player_filename, player_info_is_good, tests
    return datainfo, datafile_name, player_info_is_good, tests


def buttons(de_x, de_y, button_starti, button_methodi, button_reresti, button_restarti, button_resumei, button_jstarti, button_maini, button_pausei, button_testi):
    # button_start = AS.Button(1400, 700, button_starti, 370, 120) method 버튼 없어져서 위치 안맞음
    button_start = AS.Button(1400, 770, button_starti, 370, 120)
    
    button_start2 = AS.Button(de_x/2-165,900, button_starti, 370, 120)
    button_start3 = AS.Button(de_x/2-(165*3),900, button_starti, 370, 120)
    button_method = AS.Button(1400, 840, button_methodi, 370, 120)
    button_rerest = AS.Button(de_x/2+165,900, button_reresti, 370, 120)
    button_restart = AS.Button(de_x*0.5-185, de_y*0.64, button_restarti, 370, 120)
    # button_restart2 = AS.Button(580,830, button_restarti, 370, 120) # 블락버전으로 바꾸려구!
    button_restart2 = AS.Button(580,830, button_resumei, 370, 120)
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


def intro(screen, background_img, title_gold, title_word, miner_intro, cart_full, button_method, button_start, game_status, game_status_old, datainfo):
    screen.blit(background_img, (0, 0))
    screen.blit(title_gold, (1100, 70)) # 1050,40
    screen.blit(title_word, (1200, 50))
    screen.blit(miner_intro, (140, 250))
    screen.blit(cart_full, (750, 450))

    # Resting 측정 후 Methods가 나오도록 변경 예정.
    # if button_method.draw(screen):
    #     game_status_old = game_status
    #     game_status = "method"

    # 게임 시작 버튼을 그리면서 버튼이 눌릴때 게인 status의 변화를 유발 한다.
    if button_start.draw(screen):
        game_status_old = game_status
        if datainfo.restEver[datainfo.session_num-1] == False:
            game_status = "rest_method"
        else:
            game_status = "method";
    
    return game_status, game_status_old, datainfo


def method(screen, game_status, game_status_old, de_x, de_y, method_back, button_start2, method):
    screen.blit(method_back, (0, 0))
    screen.blit(method, ((de_x-1400)/2, 100))
    connection_check = True
    if button_start2.draw(screen):
        game_status_old = game_status
        game_status = "game_start"
        connection_check = False;
    return game_status, game_status_old, connection_check


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


def resting(screen, game_status, game_status_old, de_x, de_y, resting_back, rest_ins, all_sprites, button_jstart, resting_start, eye_1, mt, base_result, rpy, times,  test_mode, datainfo, temp_EEG):# resting_eye):

    # print("resting_start is ", resting_start)

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
    # print("times: ", times)

    # 3초 (RESTING_EYE 디폴트 값) 이전:
    # print("eye animation duration: ", T.RESTING_EYE)

    if cumtime < T.RESTING_EYE:
        AS.resting_eye_play(screen, all_sprites, mt)
        if button_jstart.draw(screen):
            print(datainfo.baseline_FAA[0], datainfo.baseline_FAA[1])

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
        
        # EEG saving
        # temp_EEG;eeg_temp;
        time_temp2 = temp_buffer[4, -EC.fft_win_len:];
        
        temp_EEG = EC.eeg_datasaving(temp_EEG, eeg_temp, time_temp2);
        
        
        
        
        
    else:
        faa_mean = np.mean(np.array(base_result)[:, 0])
        faa_std = np.std(np.array(base_result)[:, 0])
        session_num = datainfo.session_num;
        datainfo.baseline_FAA[session_num-1][0] = faa_mean;
        datainfo.baseline_FAA[session_num-1][1] = faa_std;
        datainfo.restEver[session_num-1] = True;
        
        if test_mode:
            faa_mean = -0.7
            faa_std = 0.1
            session_num = datainfo.session_num;
            datainfo.baseline_FAA[session_num-1][0] = faa_mean;
            datainfo.baseline_FAA[session_num-1][1] = faa_std;
            datainfo.restEver[session_num-1] = True;
        
        # resting_num = resting_num + 1
        game_status_old = game_status
        # 결과 페이지 상태 설정
        game_status = "rest_result"
        
        

    return game_status, game_status_old, resting_start, base_result, datainfo, temp_EEG


def rest_result(screen, game_status, game_status_old, de_x, de_y, resting_back, rest_rep, button_start3, button_rerest, datainfo):
    screen.blit(resting_back, (0, 0))
    screen.blit(rest_rep, ((de_x-1000)/2, 70))
    session_num = datainfo.session_num;
    mean_word = 'Mean : ' + str(round(datainfo.baseline_FAA[session_num-1][0], 2))
    std_word ='Std : ' + str(round(datainfo.baseline_FAA[session_num-1][1], 2))
    
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
        
    return game_status, game_status_old, datainfo


def gaming(screen, game_status, game_status_old, de_x, de_y,  game_back, game_rd, game_st, game_stop,
           game_pauseb, pause_title, button_pause, button_resume, button_main, button_restart, times, nf_result, rpy, game_stat,
           game_stbar, cart_group, miner_set, game_rock, game_reward, mt, miner_sprites, ani_start, ani_frame, test_mode,
           game_ready, game_bound, game_bound_old, draw_reward, bound_time, index_num, reward_frame, stage_result, reward_num, datainfo, add_frame, stage_bounds, temp_EEG):
# def gaming(screen, game_status, game_status_old, de_x, de_y, faa_mean, faa_std, game_back, game_rd, game_st, game_stop, game_pauseb, pause_title, button_resume, button_main, button_restart, times, nf_result, rpy, game_stat, game_stbar, cart_group, miner_set, game_rock, game_reward, mt):
    # background 
    # global ani_start
    # reward_num = 0
    starting_time = 4
    # game_bound = 0
    # game_bound_old = 0
    session_num = datainfo.session_num;
    faa_mean  = datainfo.baseline_FAA[session_num-1][0];
    faa_std =  datainfo.baseline_FAA[session_num-2][1];
    block_num = datainfo.stagenum;
    
    # setting timers
    if game_st is False:
        game_st = True
        cumtime = 0
        curtime = time.time()
        times = [[round(cumtime, 3), round(curtime, 3)], [round(cumtime, 3), round(curtime, 3)]];
        #print(game_st)
       
    elif time.time() - times[0][1] > starting_time:
        cumtime = time.time() - times[0][1]
        curtime = time.time();
        times = [[round(cumtime, 3), round(curtime, 3)], [round(cumtime, 3), round(curtime, 3)]];
    
    screen.blit(game_back, (0, 0))
    # print(times)
    # print(times[0][0] - times[1][0])
    
    
    # there's a blank screen for 2 seconds
    # finally let's start the game!!!
    if times[0][0] > starting_time and game_st is True:
        # REWARD 누적 된 거
        # ani_start = False

        if game_stop:
            # game stop 이라면
            screen.blit(game_pauseb, (de_x*0.025, de_y*0.05))
            screen.blit(pause_title, (de_x*0.5-275, de_y*0.2))
            
            # bound plot 저장
            bound_savefname = datainfo.folder_path + '/stage_summary_s' + str(datainfo.session_num) + '_b' +str(datainfo.stage_num) +'.png'
            print('save line plot ...')
            EC.bound_line_plot_save(stage_bounds, bound_savefname)
            
            if button_resume.draw(screen):
                game_stop = False
            if button_main.draw(screen):
                game_status = "intro"
                game_stop = False
            if button_restart.draw(screen):
                game_status = "game_start"
                game_st = False
                game_stop = False
                
            # neurofeedback FAA 저장
            nf_faa_mean = np.mean(np.array(nf_result)[:, 0])
            datainfo.NF_FAA_mean[session_num-1][block_num-1] = nf_faa_mean;

        else: # game stop이 아니라면
            # [UPDATE FOR FAA]
            # -> add new faa data into nf_result
            # -> return new statbar_loc
            temp_curtime = time.time();
            if times[0][1] - temp_curtime <= T.NF_update_t:  
                # baseline faa
                faa_mean; faa_std;
                # NF faa calc
                temp_buffer = np.array(rpy.root.data_storage);
                time_temp = temp_buffer[4,-int(EC.fft_win_len/2)];
                # online-processing 1. epoching with the newest data
                eeg_temp = temp_buffer[:2,-EC.fft_win_len:];
                # online-processing 2. preprocessing
                eeg_rejected = EC.preprocessing(eeg_temp, EC.filter_range, EC.noise_thr,EC.srate)
                # calculate FAA using fft
                raw_faa = EC.calc_asymmetry(eeg_rejected, EC.fft_win_len, EC.cutOff, EC.alpha_idx_range);
                faa_z = (raw_faa - faa_mean) /faa_std; # z-score the raw faa by baseline faa
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
                
                # EEG saving
                # temp_EEG;eeg_temp;
                time_temp2 = temp_buffer[4, -EC.fft_win_len:];
                
                temp_EEG = EC.eeg_datasaving(temp_EEG, eeg_temp, time_temp2);
                
                
                
            # [UPDATE FOR ANIMATION]
            # -> return new game_bound
            temp_curtime = time.time();
            if times[1][1] - temp_curtime <= T.anim_update_t:  # time update for anim_update
                n_avgfaa = round(T.anim_update_t / T.NF_update_t);
                
                if len(nf_result) <n_avgfaa:
                    temp_faas = np.array(nf_result)[:, 0] 
                else:
                    temp_faas = np.array(nf_result[-1*n_avgfaa:])[:, 0] 
                avgfaa = np.nanmean(temp_faas)
            
                faa_z = (avgfaa - faa_mean) /faa_std; # z-score the raw faa by baseline faa
                # game_bound_old = game_bound
                game_faa, game_bound = game_faa_convert(faa_z, de_x, de_y)
                stage_bounds.append([stage_bounds, cumtime])
                if test_mode:
                    game_bound = 4
                    # game_bound = random.randrange(0,4)


            # stat_barcolor, miner, rock, cart, reward
            screen.blit(game_stat[game_bound],(de_x*0.5-297.5, 50))
            screen.blit(game_stbar, statbar_loc)

            # reward 몇개 얻었는지 계산.. 이건 나중에하자! 일단 밑에 카트는 다 half로
            cart_num = 0
            
            
            if stage_result[0] + stage_result[1] > 20:
                cart_num = 2
            elif stage_result[0] + stage_result[1] > 10:
                cart_num = 1
            else:
                cart_num = 0
            
            # if game_bound > 2:
    
#     if game_bound_old != 3 or game_bound_old != 4 :
#         bound_st = temp_curtime
#     else:
#         bound_now = temp_curtime
#         bound_cum = bound_now - bound_st
    
#     if bound_cum >= 10: # positive 한 상태 10초 이상 유지
#         reward_select = 2
#     elif reward_select != 2 and bound_cum < 10:
#         reward_select = 1
    
    
#     if reward_select == 1:
#         draw_reward = game_reward[0]
    
#     elif reward_select == 2:
#         draw_reward = game_reward[1]
    
#     draw_reward = pygame.transform.rotate(draw_reward, random.randint(1,4)*90)
    
            # print(ani_start)
            if ani_start:
                
                ani_start, ani_frame, index_num, reward_frame, stage_result, add_frame = AS.miner_ani_starter(screen, miner_sprites, game_bound, mt, game_rock, de_x, de_y, draw_reward, reward_num, cart_group, cart_num, ani_frame, index_num, reward_frame, stage_result, game_bound, add_frame)
                # print(reward_num)
                
            elif game_bound == 3 or game_bound == 4:
                ani_start = True
                ani_frame = 0
                reward_frame = 0
                
                draw_reward, bound_time, reward_num = miner_animate(game_bound, game_bound_old, temp_curtime, game_reward, draw_reward, bound_time, reward_num)
                # print(reward_num)
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
            
            # else:
            #     screen.blit(miner_set[3],(690, 205))

            # else:
            #     # reward_select = 1 # 1 gold 2 dia
            #     ani_start = True
            #     ani_frame = 0
            
            
            
            # reward_select = 1 # reward - faa positive 하게 유지되는 시간 재서 결정해야함 (지금은 일단 ㄱㄱ)
            # reward_add = 0
            # ani_start = True
            
            # if reward_select == 1:
            #     draw_reward = game_reward[0]
            # elif reward_select == 2:
            #     draw_reward = game_reward[1]
            # draw_reward = pygame.transform.rotate(draw_reward, random.randint(1,4)*90)

            # if ani_start == True:
                
                
            #     ani_start, ani_frame = AS.miner_ani_starter(screen, miner_sprites, game_bound, mt, game_rock, de_x, de_y, draw_reward, cart_group, cart_num, ani_frame)
                
                # if still_ani:
                    
                # else:
                    # ani_start = False
            # print(game_bound_old, game_bound)
            game_bound_old = game_bound
            

            # game_animation(game_bound)
            if times[0][0] > T.NF_T:
                # game stop
                game_stop = True
                game_status = "game_result"
                
            if button_pause.draw(screen):
                game_stop = True    
            
        
    # else:
    
    
    # stage number
    elif time.time() - times[0][1] < 2:
        screen.blit(game_pauseb, (de_x*0.025, de_y*0.05))
        block_word = 'Stage ' + str(block_num)
        
        font6 = pygame.font.SysFont('arial', 250, True)
        for_block = font6.render(block_word, False, 'White')
        block_x, block_y = for_block.get_size()
        
        screen.blit(for_block, ((de_x-block_x)/2, (de_y-block_y)/2))
        # screen.blit(for_std, ((de_x-std_x)/2, 500+(std_y/1.5)))
        
    # ready
    else:
        screen.blit(game_rock,(de_x-600, de_y-600))
        # miner
        screen.blit(miner_set[3],(690, 205))
        # cart
        screen.blit(cart_group[0],(de_x/2-950, de_y-625))
        # ready
        screen.blit(game_ready, (de_x/2-900,de_y-800))
        
        

    return game_status, game_status_old, stage_result, game_rd, game_st, game_stop, times, nf_result, ani_start, ani_frame, game_bound, game_bound_old, draw_reward, bound_time, index_num, reward_frame, reward_num, datainfo, add_frame, stage_bounds, temp_EEG


def miner_animate(game_bound, game_bound_old, temp_curtime, game_reward, draw_reward, bound_time, reward_num):
    
    if game_bound_old < 3 :
        bound_time[0] = temp_curtime
        # bound_st = temp_curtime
    else:
        bound_time[1] = temp_curtime
        # bound_time[2] = bound_now - bound_st
        bound_time[2] = bound_time[1] - bound_time[0]

        # bound_now = temp_curtime
        # bound_sum = bound_now - bound_st
        # print(bound_time[2])
        draw_reward = game_reward[0]
        reward_num = 1
        
        if bound_time[2] >= 10:
            # reward_select = 2
            # print('1')
            draw_reward = game_reward[1]
            draw_reward = pygame.transform.rotate(draw_reward, random.randint(1,4)*90)
            bound_time[0] = temp_curtime
            reward_num = 2
        elif draw_reward != game_reward[1] and bound_time[2] < 10: # reward_select !=2 and bound_time[2] < 10: #bound_sum < 10:
            # reward_select = 1
            # print('2')
            draw_reward = game_reward[0]
            draw_reward = pygame.transform.rotate(draw_reward, random.randint(1,4)*90)
            reward_num = 1
            
    # AS.miner_ani_starter
    
    # animation_end = False
    # if animation_end:
    #     miner_wait = False
    # else:
    #     miner_wait = True
    
    # print(reward_num)
    # print(bound_time[2])
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
        statbar_loc = (de_x*0.5-297.5-15+(595*(0.5+0.2*game_faa)), 50-7.5) # range에 따라 계속 다시 계산해야 지금은 -2 ~ 2 기준
    
    
    return game_faa, statbar_loc


def game_faa_convert(faa_z, de_x, de_y):
    #game_faa_range = [-1, 1]
    #game_unit = game_faa_range/5
    #bound_range = [game_unit*(-5), game_unit*(-3), game_unit*(-1), game_unit*(1), game_unit*(3), game_unit*(5)]

    max_faa_std = T.max_faa_std; # = 2
    game_unit = np.linspace((-1)*max_faa_std, max_faa_std, T.faa_steps); # [-2 -1.2 -0.4 0.4 1.2 2];
    bound_range = list(game_unit);
    
    if faa_z > max_faa_std:
        game_faa = max_faa_std
        # statbar_loc = (de_x*0.5-297.5-15+(595*.9), 50-7.5)
    
    elif faa_z < (-1)*max_faa_std:
        game_faa = (-1)*max_faa_std
        # statbar_loc = (de_x*0.5-297.5-15+(595*.1), 50-7.5)
    
    else:
        game_faa = faa_z
        # statbar_loc = (de_x*0.5-297.5-15+(595*(0.5+0.2*game_faa)), 50-7.5) # range에 따라 계속 다시 계산해야 지금은 -2 ~ 2 기준
    
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
    
    
    return game_faa, game_bound #, statbar_loc



def game_result(screen, game_status, game_status_old, stage_result, de_x, de_y, game_back, game_cl_b, game_cl_res, cart_result, miner_intro, game_clear, button_main2, button_restart2, datainfo):
    block_num = datainfo.stagenum;
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
    
    print_counter_game_start = None;
    if button_main2.draw(screen):
        game_status_old = game_status
        game_status = "intro"
    if button_restart2.draw(screen):
        game_status_old = game_status
        game_status = "game_start"
        print_counter_game_start = False;
    if datainfo.stagenum > 5:
        game_status_old = game_status
        game_status = "GameEnd"
    
    return game_status, game_status_old, print_counter_game_start, datainfo




