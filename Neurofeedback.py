# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 16:06:59 2023

@author: JISU
"""
import pygame
from datetime import datetime

import assets as button


class Neurofeedback:
    
    def __init__(self):
        self.screen_size = (1920,1080)
        
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
 
    
    def game_init():
        # start pygame
        pygame.init()
        
        # 
        pygame.display.set_caption("leelab_Neurofeedback")
        
        
        
        #screen size setting
        
        screen_size = (1920,1080)
        screen = pygame.display.set_mode(screen_size)
        
        
        # get screen size
        de_x, de_y = screen.get_size()
        print(de_x, de_y)
        
        
        # clock - for game loop (fps)
        clock= pygame.time.Clock()
        
        run = True
        game_starter = False
        
        # words 
        font6 = pygame.font.SysFont('arial',50, True)
        for_start = font6.render('Press SPACE to start', False, 'White')
        font_x, font_y = for_start.get_size()
        
        
        
        while run:
            
            # processing inputs
            for event in pygame.event.get():
        
                keys_act = pygame.key.get_pressed()
                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()
                
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                   
                if keys_act[pygame.K_ESCAPE]:
                    run = False
                
                if keys_act[pygame.K_SPACE]:
                    game_starter = True
                
        
                    
            # if game_starter:
                # intro(de_x, de_y)
                # print("ok")
                
            # else:    
            screen.fill((100, 100, 110))
            screen.blit(for_start, ((de_x-font_x)/2, 500))
        
            
            
            pygame.display.update()
            
            # fps
            clock.tick(60)
        
        
        pygame.quit()       



# def intro(de_x, de_y):
#     background_img = pygame.image.load('IMAGES/picset/background.jpg').convert_alpha() 
#     background_img = pygame.transform.scale(background_img, (de_x, de_y))
    
#     title_gold = pygame.image.load('IMAGES/picset/title_gold.png').convert_alpha() 
#     title_gold = pygame.transform.scale(title_gold, (900, 450))
#     title_word = pygame.image.load('IMAGES/picset/title_word.png').convert_alpha() 
#     title_word = pygame.transform.scale(title_word, (580, 290))
        
#     miner_intro = pygame.image.load('IMAGES/picset/character/miner_intro.png').convert_alpha() 
#     miner_intro = pygame.transform.scale(miner_intro, (700, 800))
    
    
#     cart_full = pygame.image.load('IMAGES/picset/cart/cart_2.png').convert_alpha() 
#     cart_full = pygame.transform.scale(cart_full, (600, 600))
        
#     screen.blit(background_img,(0,0))
#     screen.blit(title_gold,(1050,40))
#     screen.blit(title_word,(1200,50))
#     screen.blit(miner_intro,(140,250))
#     screen.blit(cart_full,(750,450))
    
    


# # def method():
# #     screen.blit(method_back,(0,0))
# #     screen.blit(method,((de_x-1400)/2,100))






# def game_init():
#     # start pygame
#     pygame.init()
    
#     # 
#     pygame.display.set_caption("leelab_Neurofeedback")
    
    
    
#     #screen size setting
    
#     screen_size = (1920,1080)
#     screen = pygame.display.set_mode(screen_size)
    
    
#     # get screen size
#     de_x, de_y = screen.get_size()
#     print(de_x, de_y)
    
    
#     # clock - for game loop (fps)
#     clock= pygame.time.Clock()
    
#     run = True
#     game_starter = False
    
#     # words 
#     font6 = pygame.font.SysFont('arial',50, True)
#     for_start = font6.render('Press SPACE to start', False, 'White')
#     font_x, font_y = for_start.get_size()
    
    
    
#     while run:
        
#         # processing inputs
#         for event in pygame.event.get():
    
#             keys_act = pygame.key.get_pressed()
#             mouse = pygame.mouse.get_pos()
#             click = pygame.mouse.get_pressed()
            
            
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()
               
#             if keys_act[pygame.K_ESCAPE]:
#                 run = False
            
#             if keys_act[pygame.K_SPACE]:
#                 game_starter = True
            
    
                
#         if game_starter:
#             intro(de_x, de_y)
#             # print("ok")
            
#         else:    
#             screen.fill((100, 100, 110))
#             screen.blit(for_start, ((de_x-font_x)/2, 500))
        
        
        
#         pygame.display.update()
        
#         # fps
#         clock.tick(60)
    
    
#     pygame.quit()