# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 16:06:59 2023

@author: JISU
"""
import pygame
from datetime import datetime
import os
# import assets as button
# from assets import Button
import assets as AS
import GameProcess as GP
from Connection import Connect
import rpyc
import time
from DataInfo import DataInfo
import numpy as np
import pandas as pd
import pickle
class Neurofeedback:
    def __init__(self, datainfo, test_mode):
    # def __init__(self, player_id, player_session, player_block, manual_faa_mean, manual_faa_std, player_datafile, test_mode):

        # self.player_id = datainfo.player_id
        #self.player_session = datainfo.session_num
        # self.player_block = datainfo.stagenum
        self.datainfo = datainfo
        self.connect = Connect() 
        self.rpy = None
        self.test_mode = test_mode
        
        # start pygame
        pygame.init()
        
        # 
        pygame.display.set_caption("leelab_Neurofeedback")
        
        print()

        # screen size setting
        screen_size = (1920, 1080)
        self.screen = pygame.display.set_mode(screen_size)
        
        # get screen size
        de_x, de_y = self.screen.get_size()
        print(de_x, de_y)
        
        # clock - for game loop (fps)
        clock = pygame.time.Clock()
        mt = clock.tick(60) / 800  # for resting frame num
        cumtime = 0
        curtime = 0
        times = [cumtime, curtime]
        run = True
        # block_num = 1 # -> datainfo.stagenum
        
        game_starter = True  # default is True
        game_st = False  # default is False
        resting_start = False  # default is False
        base_result = []
        nf_result = []
        temp_EEG = np.array([]);
        game_rd = True
        game_stop = False
        # faa_mean = 0 # -> datainfo.baseline_FAA[0]
        # faa_std = 0 # -> datainfo.baseline_FAA[1]
        ani_start = False
        ani_frame = 0
        reward_frame = 0
        # resting_num = 0 #  -> datainfo.session_num
        game_bound = 0
        game_bound_old = 0
        bound_time = [0,0,0]
        index_num = 0
        stage_result = [0, 0]
        reward_num = 1
        add_frame = 0
        # newly added one
        current_session = 1

        # words 
        font6 = pygame.font.SysFont('arial', 50, True)
        for_start = font6.render('Press SPACE to start', False, 'White')
        font_x, font_y = for_start.get_size()
        
        # 230626 return button & session result title img added (temp img)
        # buttons
        button_starti, button_oldsessioni, button_reresti, button_restarti, button_resumei, button_jstarti, button_maini, button_pausei, button_testi, button_returni, button_resulti, button_byei = AS.button_img()
        button_start, button_start2, button_start3, button_oldsession, button_rerest, button_restart, button_restart2, button_resume, button_jstart, button_main, button_main2, button_pause, button_right, button_left, button_up, button_down, button_test, button_return, button_result, button_s2start, button_main3, button_bye = GP.buttons(de_x, de_y, button_starti, button_oldsessioni, button_reresti, button_restarti, button_resumei, button_jstarti, button_maini, button_pausei, button_testi, button_returni, button_resulti, button_byei)
        # images
        background_img, method_back, resting_back, game_back, title_gold, title_word, rest_title, pause_title, method, rest_ins, rest_expl, rest_rep, game_pauseb, game_cl_b, game_cl_res, game_clear, prev_session, session_worimg = AS.back_img(de_x, de_y)
        # objects
        miner_intro, miner_result = AS.miner_img()
        cart_full = AS.cart_img()
        
                
        # 230626 added ================================================================================================================
        #result example images
        stage_temp_result, session_result1, session_result2 = AS.graph_img()
        # ========================================================================================================================    
        
        
        
        game_stat, game_stbar, cart_group, miner_set, game_rock, game_reward, game_ready = AS.gaming_img()
        
        resting_eye = AS.resting_eye((de_x/2-800, de_y/2-220))
        # self.all_sprites = pygame.sprite.Group(resting_eye)
        miner_ani = AS.miner_animation()
        # self.miner_sprites = pygame.sprite.Group(miner_ani)

        eye_1 = pygame.image.load('IMAGES/picset/resting/eye1.png').convert_alpha()
        eye_1 = pygame.transform.scale(eye_1, (1600, 560))
        
        connection_check = True
        draw_reward = game_reward[0]

        # just some counters for text display.
        print_counter_starter = False
        print_counter_intro = False
        print_counter_method = False
        print_counter_rest_method = False
        print_counter_rest_start = False
        print_counter_rest_result = False
        print_counter_game_start = False
        print_counter_game_result = False
        # newly added pages
        print_counter_session_result = False    
        print_counter_all_session = False


        game_status_old = "null"
        game_status = "intro"

            
        while run:
            # processing inputs
            for event in pygame.event.get():
        
                keys_act = pygame.key.get_pressed()
                # mouse = pygame.mouse.get_pos()
                # click = pygame.mouse.get_pressed()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                   
                if keys_act[pygame.K_ESCAPE]:
                    run = False
                
                # 게임 시작 스페이스바
                #if keys_act[pygame.K_SPACE]:

                # game_status = "game_start"
                # faa_mean = 0
                # faa_std = 0

            if game_starter:
                # if print_counter_starter == False:
                #     print("게임 시작합니다. 서버 접속 중")
                #     print_counter_starter = True
                # Connection check
                # 1) before baseline, 2) before main_game
                # print(connection_check)
                if connection_check == False:
                    self.rpy, connection_check = self.connect.check(connection_check)
                    print('Connected to EEG data server')
                    
                # Game process
                # 첫 인트로 화면
                elif game_status == "intro":
                    if print_counter_intro == False:
                        print("게임 인트로 시작")
                        print_counter_intro = True

                    game_status, game_status_old, self.datainfo = GP.intro(self.screen, background_img, title_gold, title_word, miner_intro, cart_full, button_oldsession, button_start, game_status, game_status_old, self.datainfo, button_s2start)
                    # print(connection_check)

                # 230626 added screen (all session results) ==========================================================================
                elif game_status == "all_session":
                    if print_counter_all_session == False:
                        print("이전 세션 결과")
                        print_counter_all_session = True

                    game_status, game_status_old, current_session = GP.all_session(self.screen, game_status, game_status_old, de_x, de_y,
                                                                  game_back, game_cl_b, button_return, prev_session,
                                                                  session_result1, session_result2, self.datainfo,
                                                                  current_session, button_right, button_left)
                #==================================================================================================================

                # resting state 안내문
                elif game_status == "rest_method":
                    if print_counter_rest_method == False:
                        print("휴지기 뇌파 측정 설명 시작")
                        print_counter_rest_method = True
                        
                    game_status, game_status_old, connection_check = GP.rest_method(self.screen, game_status, game_status_old, de_x, de_y, resting_back, rest_expl, rest_title, button_jstart)
                    # print(connection_check)

                # resting state 측정하는 중
                elif game_status == "rest_start":
                    if print_counter_rest_start == False:
                        print("휴지기 뇌파 측정 시작")
                        times[1] = time.time()
                        temp_EEG = np.array([]);
                        print_counter_rest_start = True

                    all_sprites = pygame.sprite.Group(resting_eye)
                    game_status, game_status_old, resting_start, base_result,  self.datainfo, temp_EEG = \
                        GP.resting(self.screen, game_status, game_status_old, de_x, de_y, resting_back, rest_ins,
                                   all_sprites, button_jstart, resting_start, eye_1, mt,  base_result, self.rpy,
                                   times,  test_mode, self.datainfo, temp_EEG)#, resting_eye )

                    pygame.display.update()

                # resting state 다한 뒤 결과
                elif game_status == "rest_result":
                    if print_counter_rest_result == False:
                        print("휴지기 뇌파 측정 결과 제시")
                        print("BASELINE 데이터 저장 중...")
                        
                        # resting 결과 저장
                        session_num = self.datainfo.session_num;
                        # 1. continuous FAA
                        self.datainfo.base_FAA_result[session_num-1] = base_result;
                        
                        # 2. MEAN/STD FAA
                        # -> GP.resting
                        
                        # 3.raw_EEG 저장 into csv
                        base_result_fname = self.datainfo.eeg_path + '/baseEEG_s' + str(session_num)+'.csv';
                        temp_EEG=np.transpose(temp_EEG);
                        EEG_df = pd.DataFrame(temp_EEG, columns = ['Left_ch','Right_ch','time'])
                        EEG_df.to_csv(base_result_fname, sep=',')
                        
                        #raw data path 저장
                        self.datainfo.EEG_path_baseline[session_num-1] = base_result_fname;
                        
                        # 4. pickle 저장
                        with open(file= self.datainfo.save_path, mode='wb') as f:
                            pickle.dump(self.datainfo, f)
                            
                        print_counter_rest_result = True
                    # del all_sprites
                    game_status, game_status_old, self.datainfo = GP.rest_result(self.screen, game_status, game_status_old, de_x, de_y,
                                                                  resting_back, rest_rep, button_start3,
                                                                  button_rerest, self.datainfo)

                # 게임 인스트럭션 부분
                elif game_status == "method":
                    if print_counter_method == False:
                        print("게임 설명 시작")
                        print_counter_method = True
                    game_status, game_status_old, connection_check = GP.method(self.screen, game_status, game_status_old, de_x, de_y,
                                                             method_back, button_start2, method)
                    # print(connection_check)
                    print_counter_game_start = False;
                # miner 게임 작동화면
                elif game_status == "game_start":
                    if print_counter_game_start == False:
                        stage_result = [0, 0]
                        stage_bounds = [];
                        temp_EEG = np.array([]);
                        print("뉴로피드백 블록 시작")
                        # times[1] = time.time()
                        # reset the timer 
                        # -> times[0] : timer for FAA calc.
                        # -> times[1] : timer for animation update.
                        times = [[cumtime, curtime], [cumtime, curtime]];
                        print_counter_game_start = True;
                    miner_sprites = pygame.sprite.Group(miner_ani)
                    game_status, game_status_old, stage_result, game_rd, game_st, game_stop, times, nf_result, ani_start,\
                    ani_frame, game_bound, game_bound_old, draw_reward, bound_time, index_num, reward_frame, reward_num, self.datainfo, add_frame, stage_bounds,temp_EEG = GP.gaming(self.screen,
                                          game_status, game_status_old, de_x, de_y, 
                                          game_back, game_rd, game_st, game_stop, game_pauseb, pause_title, button_pause, 
                                          button_resume, button_main, button_restart, times, nf_result, self.rpy,
                                          game_stat, game_stbar, cart_group, miner_set, game_rock, game_reward, mt,
                                          miner_sprites, ani_start , ani_frame, self.test_mode, game_ready, game_bound, game_bound_old, draw_reward, bound_time, index_num, reward_frame, stage_result, reward_num, self.datainfo, add_frame, stage_bounds,temp_EEG)
                    # game_status, game_status_old, game_result, game_rd, game_st, game_stop, times, nf_result = GP.gaming(self.screen, game_status, game_status_old, de_x, de_y, faa_mean, faa_std, game_back, game_rd, game_st, game_pauseb, pause_title, button_resume, button_main, button_restart, times, nf_result, self.rpy, game_stat, game_stbar, cart_group, miner_set, game_rock, game_reward, mt)
                    
                    # game_status, game_status_old, game_result, game_rd, game_st, game_stop, times, nf_result = GP.gaming2(self.screen, game_status, game_status_old, de_x, de_y, faa_mean, faa_std, game_back, game_rd, game_st, game_stop, game_pauseb, pause_title, button_resume, button_main, button_restart, times, nf_result, self.rpy, game_stat, game_stbar)
                    print_counter_game_result = False;
                # miner 게임 작동 결과
                elif game_status == "game_result":
                    if print_counter_game_result == False:
                        print("뉴로피드백 블록 결과 제시")
                        print(stage_result)
                        print_counter_game_result = True

                        # NF 후 결과 저장 (save datainfo in pickle) 
                        session_num = self.datainfo.session_num;
                        stagenum = self.datainfo.stagenum;
                        # self.datainfo.NF_FAA_fname[self.datainfo.stagenum-1] = nf_result_fname;
                        # 1. continuous FAA
                        self.datainfo.NF_FAA_result[session_num-1][stagenum-1] = nf_result;
                        # 2. MEAN/STD FAA
                        # -> GP.gaming
                        # 3. stage results & bounds
                        self.datainfo.stage_result[session_num-1][stagenum-1][0] = stage_result[0];
                        self.datainfo.stage_result[session_num-1][stagenum-1][1] = stage_result[1];
                        self.datainfo.stage_bounds[session_num-1][stagenum-1] = stage_bounds;
                        
                        # 4. Raw EEG
                        nf_result_fname = self.datainfo.eeg_path + '/nfEEG_s'+str(session_num)+'_b'+str(stagenum-1) +'.csv';
                        temp_EEG=np.transpose(temp_EEG);
                        EEG_nf_df = pd.DataFrame(temp_EEG, columns = ['Left_ch','Right_ch','time'])
                        EEG_nf_df.to_csv(nf_result_fname, sep=',')
                        
                        #raw data path 저장
                        self.datainfo.EEG_path_game[session_num-1][stagenum-1] = nf_result_fname;
                        
                        # Block number update
                        self.datainfo.stagenum = self.datainfo.stagenum+1; 
                        
                        # 5. pickle 저장 save
                        with open(file= self.datainfo.save_path, mode='wb') as f:
                            pickle.dump(self.datainfo, f)

                            
                    game_status, game_status_old, \
                    print_counter_game_start, self.datainfo = GP.game_result(self.screen,game_status, game_status_old,
                                                                             stage_result, de_x, de_y, game_back, game_cl_b,
                                                                             game_cl_res, cart_full, miner_result, game_clear,
                                                                             button_main2, button_restart2, stage_temp_result, self.datainfo, button_result)
                    game_rd = True
                    game_st = False
                    game_stop = False


                    
                # 230626 added screen ===========================================================================================
                elif game_status == "session_result":
                    if print_counter_session_result == False:
                        print("이번 세션 결과")
                        print_counter_session_result = True
                    
                    # 마지막에 session_result1, session_result2는 data 이용해서 만들어야 함 *일단 이렇게 대충 아무사진이나 넣어서 배치만!
                    game_status, game_status_old = GP.session_result(self.screen, game_status, game_status_old, de_x, de_y,
                                                                     game_back, game_cl_b, button_main3, session_worimg,
                                                                     self.datainfo, game_clear, session_result1,
                                                                     session_result2, button_bye)


                #==================================================================================================================
                   
                
                # 이거 연결된 것도 없구...나중에 다른 버튼이랑 연결시켜서 해야할듯
                elif game_status == "GameEnd":
                    print("겜끝!")
                    '''
                    이부분 필요없을 것 같아서 일단 없애놓음
                    # session num and block num edit
                    self.datainfo.stagenum = 1;
                    self.datainfo.session_num =self.datainfo.session_num + 1;
                    ''' 
                    
                    pygame.quit()
            
            # 인트로 이전 PRESS SPACE TO START 화면
            else:
                pass
                # self.screen.fill((100, 100, 110))
                # self.screen.blit(for_start, ((de_x-font_x)/2, 500))
                #
            pygame.display.update()
            
            # 60 fps로 유지
            clock.tick(60)
        
        pygame.quit()
 
