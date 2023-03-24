# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 16:06:59 2023

@author: JISU
"""
import pygame
from datetime import datetime

# import assets as button
# from assets import Button
import assets as AS
import GameProcess as GP
from Connection import Connect
import rpyc


class Neurofeedback:
    def __init__(self, player_id, player_session, player_datafile):

        self.player_id = player_id
        self.player_session = player_session
        self.player_datafile =player_datafile
        self.connect = Connect()
        self.rpy = None
        
        # start pygame
        pygame.init()
        
        # 
        pygame.display.set_caption("leelab_Neurofeedback")
        
        print()
        
        #screen size setting
        
        screen_size = (1920, 1080)
        self.screen = pygame.display.set_mode(screen_size)
        
        
        # get screen size

        de_x, de_y = self.screen.get_size()
        print(de_x, de_y)
        
        
        # clock - for game loop (fps)
        clock= pygame.time.Clock()
        mt = clock.tick(60) / 800  # for resting frame num
        cumtime = 0;
        curtime = 0;
        times = [cumtime, curtime];
        run = True
        game_starter = False
        resting_start = False
        base_result = []
        nf_result = [];
        game_rd = True
        game_st = False
        game_stop = False
        faa_mean = 0
        faa_std = 0
        ani_start = True
        ani_frame = 0
        resting_num = 0
        
        # words 
        font6 = pygame.font.SysFont('arial',50, True)
        for_start = font6.render('Press SPACE to start', False, 'White')
        font_x, font_y = for_start.get_size()
        
        # buttons
        button_starti, button_methodi, button_reresti, button_restarti, button_resumei, button_jstarti, button_maini, button_pausei, button_testi = AS.button_img()
        button_start, button_start2, button_start3, button_method, button_rerest, button_restart, button_restart2, button_resume, button_jstart, button_main, button_main2, button_pause, button_right, button_left, button_up, button_down, button_test = GP.buttons(de_x, de_y, button_starti, button_methodi, button_reresti, button_restarti, button_resumei, button_jstarti, button_maini, button_pausei, button_testi)
        # images
        background_img, method_back, resting_back, game_back, title_gold, title_word, rest_title, pause_title, method, rest_ins, rest_expl, rest_rep, game_pauseb, game_cl_b, game_cl_res, game_clear = AS.back_img(de_x, de_y)
        # objects
        miner_intro = AS.miner_img()
        cart_full = AS.cart_img()
        
        game_stat, game_stbar, cart_group, miner_set, game_rock, game_reward = AS.gaming_img()
        

        resting_eye = AS.resting_eye((de_x/2-800,de_y/2-220))
        # self.all_sprites = pygame.sprite.Group(resting_eye)
        miner_ani = AS.miner_animation()
        # self.miner_sprites = pygame.sprite.Group(miner_ani)

        
        
        eye_1 = pygame.image.load('IMAGES/picset/resting/eye1.png').convert_alpha() 
        eye_1 = pygame.transform.scale(eye_1, (1600, 560))
        
        connection_check = True;

        # 여기서부터 게임이 시작된다.
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
                
                #게임 시작 스페이스바
                if keys_act[pygame.K_SPACE]:
                    game_starter = True
                    game_status_old = "null"
                    game_status = "intro"
                    # game_status = "game_start"
                    # faa_mean = 0
                    # faa_std = 0
                
        
            
            if game_starter:
                # Connection check
                # 1) before baseline, 2) before main_game
                # print(connection_check)
                if connection_check == False:
                    self.rpy, connection_check = self.connect.check(connection_check)
                    print('hello')
                # Game process
                
                # 첫인트로 화면
                elif game_status == "intro":
                    game_status, game_status_old = GP.intro(self.screen, background_img, title_gold, title_word, miner_intro, cart_full, button_method, button_start, game_status, game_status_old)
                    # print(connection_check)
                # 게임 인스트럭션 부분
                elif game_status == "method":
                    game_status, game_status_old = GP.method(self.screen, game_status, game_status_old, de_x, de_y, method_back, button_start2, method)
                    # print(connection_check)

                # resting state 안내문
                elif game_status == "rest_method":
                    game_status, game_status_old, connection_check = GP.rest_method(self.screen, game_status, game_status_old, de_x, de_y, resting_back, rest_expl, rest_title, button_jstart)
                    # print(connection_check)

                # resting state 측정하는 중
                elif game_status == "rest_start":
                    # print('1111')
                    all_sprites = pygame.sprite.Group(resting_eye)
                    game_status, game_status_old, resting_start, base_result, times, faa_mean, faa_std, resting_num = GP.resting(self.screen, game_status, game_status_old, de_x, de_y, resting_back, rest_ins, all_sprites, button_jstart, resting_start, eye_1, mt,  base_result, self.rpy, times, faa_mean, faa_std, resting_num)#, resting_eye )
                    pygame.display.update()

                # resting state 다한 뒤 결과
                elif game_status == "rest_result":
                    # del all_sprites
                    game_status, game_status_old = GP.rest_result(self.screen, game_status, game_status_old, de_x, de_y, resting_back, rest_rep, base_result, button_start3, button_rerest, faa_mean, faa_std, resting_num)

                # miner 게임 작동화면
                elif game_status == "game_start":
                    miner_sprites = pygame.sprite.Group(miner_ani)
                    game_status, game_status_old, game_result, game_rd, game_st, game_stop, times, nf_result, ani_start, ani_frame = GP.gaming(self.screen, game_status, game_status_old, de_x, de_y, faa_mean, faa_std, game_back, game_rd, game_st, game_stop, game_pauseb, pause_title, button_resume, button_main, button_restart, times, nf_result, self.rpy, game_stat, game_stbar, cart_group, miner_set, game_rock, game_reward, mt, miner_sprites, ani_start , ani_frame)
                    # game_status, game_status_old, game_result, game_rd, game_st, game_stop, times, nf_result = GP.gaming(self.screen, game_status, game_status_old, de_x, de_y, faa_mean, faa_std, game_back, game_rd, game_st, game_pauseb, pause_title, button_resume, button_main, button_restart, times, nf_result, self.rpy, game_stat, game_stbar, cart_group, miner_set, game_rock, game_reward, mt)
                    
                    # game_status, game_status_old, game_result, game_rd, game_st, game_stop, times, nf_result = GP.gaming2(self.screen, game_status, game_status_old, de_x, de_y, faa_mean, faa_std, game_back, game_rd, game_st, game_stop, game_pauseb, pause_title, button_resume, button_main, button_restart, times, nf_result, self.rpy, game_stat, game_stbar)

                # miner 게임 작동 결과
                elif game_status == "game_result":
                    game_status, game_status_old = GP.game_result(self.screen, game_status, game_status_old, game_result, de_x, de_y, game_back, game_cl_b, game_cl_res, cart_full, miner_intro, game_clear, button_main2, button_restart2)
                    game_rd = True
                    
            else:    
                self.screen.fill((100, 100, 110))
                self.screen.blit(for_start, ((de_x-font_x)/2, 500))
        
            
            
            pygame.display.update()
            
            # fps
            clock.tick(60)
        
        
        pygame.quit()              
 
