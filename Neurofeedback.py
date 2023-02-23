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

class Neurofeedback:
    
    # def __init__(self, screen, clock, de_x, de_y):
    #     # pygame.init()
    #     # pygame.display.set_caption("leelab_Neurofeedback")
               
    #     #screen size setting
        
    #     # self.screen_size = (1920,1080)
    #     # self.screen = pygame.display.set_mode(self.screen_size)
        
    #     # get screen size
    #     # self.de_x, self.de_y = self.screen.get_size()
    #     self.clock= clock
        
    #     self.screen = screen
    #     self.de_x, self.de_y = de_x, de_y
    
    def __init__(self, player_id, player_session, player_datafile):

        self.player_id = player_id
        self.player_session = player_session
        self.player_datafile =player_datafile

        # start pygame
        pygame.init()
        
        # 
        pygame.display.set_caption("leelab_Neurofeedback")
        
        print()
        
        #screen size setting
        
        screen_size = (1920,1080)
        self.screen = pygame.display.set_mode(screen_size)
        
        
        # get screen size
        de_x, de_y = self.screen.get_size()
        print(de_x, de_y)
        
        
        # clock - for game loop (fps)
        clock= pygame.time.Clock()
        mt = clock.tick(60) / 800  # for resting frame num
        run = True
        game_starter = False
        resting_start = False
        base_result = []
        
        # words 
        font6 = pygame.font.SysFont('arial',50, True)
        for_start = font6.render('Press SPACE to start', False, 'White')
        font_x, font_y = for_start.get_size()
        
        # buttons
        button_starti, button_methodi, button_reresti, button_restarti, button_resumei, button_jstarti, button_maini, button_pausei, button_testi = AS.button_img()
        button_start, button_start2, button_start3, button_method, button_rerest, button_restart, button_restart2, button_resume, button_jstart, button_main, button_main2, button_pause, button_right, button_left, button_up, button_down, button_test = GP.buttons(de_x, de_y, button_starti, button_methodi, button_reresti, button_restarti, button_resumei, button_jstarti, button_maini, button_pausei, button_testi)
        # images
        background_img, method_back, resting_back, game_back, title_gold, title_word, rest_title, pause_title, method, rest_ins, rest_expl, rest_rep = AS.back_img(de_x, de_y)
        # objects
        miner_intro = AS.miner_img()
        cart_full = AS.cart_img()

        resting_eye = AS.resting_eye((de_x/2-800,de_y/2-220))
        # all_sprites = pygame.sprite.Group(resting_eye)
        
        eye_1 = pygame.image.load('IMAGES/picset/resting/eye1.png').convert_alpha() 
        eye_1 = pygame.transform.scale(eye_1, (1600, 560))

        
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
                
                if keys_act[pygame.K_SPACE]:
                    game_starter = True
                    game_status_old = "null"
                    game_status = "intro"
                
        
                    
            if game_starter:
                if game_status == "intro":
                    game_status, game_status_old = GP.intro(self.screen, background_img, title_gold, title_word, miner_intro, cart_full, button_method, button_start, game_status, game_status_old)
                
                elif game_status == "method":
                    game_status, game_status_old = GP.method(self.screen, game_status, game_status_old, de_x, de_y, method_back, button_start2, method)
                
                elif game_status == "rest_method":
                    game_status, game_status_old = GP.rest_method(self.screen, game_status, game_status_old, de_x, de_y, resting_back, rest_expl, rest_title, button_jstart)
                
                elif game_status == "rest_start":
                    all_sprites = pygame.sprite.Group(resting_eye)
                    game_status, game_status_old, resting_start, base_result = GP.resting(self.screen, game_status, game_status_old, de_x, de_y, resting_back, rest_ins, all_sprites, button_jstart, resting_start, eye_1, mt, base_result)#, resting_eye )
                    pygame.display.update()
                
                elif game_status == "rest_result":
                    # del all_sprites
                    game_status, game_status_old = GP.rest_result(self.screen, game_status, game_status_old, de_x, de_y, resting_back, rest_rep, base_result, button_start3, button_rerest)
                
                elif game_status == "game_start":
                    game_status, game_status_old, game_result = GP.gaming(self.screen, game_status, game_status_old, de_x, de_y)
                
                
            else:    
                self.screen.fill((100, 100, 110))
                self.screen.blit(for_start, ((de_x-font_x)/2, 500))
        
            
            
            pygame.display.update()
            
            # fps
            clock.tick(60)
        
        
        pygame.quit()              
 
    
    # def game_init():
        
    #     # start pygame
    #     pygame.init()
        
    #     # 
    #     pygame.display.set_caption("leelab_Neurofeedback")
        
    #     print()
        
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
    #             GP.intro(de_x, de_y,screen)
    #             # print("ok")
                
    #         else:    
    #             screen.fill((100, 100, 110))
    #             screen.blit(for_start, ((de_x-font_x)/2, 500))
        
            
            
    #         pygame.display.update()
            
    #         # fps
    #         clock.tick(60)
        
        
    #     pygame.quit()       



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