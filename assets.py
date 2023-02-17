# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 16:25:44 2023

@author: JISU
"""

import pygame


#button class
class Button():
	def __init__(self, x, y, image, width, height):
		self.image = pygame.transform.scale(image, (width, height))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()
		touch = False
		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			touch = True
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
        
		if touch:
			surface.blit(self.image, (self.rect.x, self.rect.y+2))
		else:
			surface.blit(self.image, (self.rect.x, self.rect.y))
                

		return action

# def images(de_x, de_y):    

    
#     # IMAGE
#     # call image
#     background_img = pygame.image.load('picset/background.jpg').convert_alpha() 
#     # transform image
#     background_img = pygame.transform.scale(background_img, (de_x, de_y))
    
    
#     method_back = pygame.image.load('picset/method/background.jpg').convert_alpha() 
#     method_back = pygame.transform.scale(method_back, (de_x, de_y))
    
#     resting_back = pygame.image.load('picset/resting/resting_back.jpg').convert_alpha() 
#     resting_back = pygame.transform.scale(resting_back, (de_x, de_y))
    
#     game_back = pygame.image.load('picset/background_22.jpg').convert_alpha() 
#     game_back = pygame.transform.scale(game_back, (de_x, de_y))
    
    
    
#     # -------------- Button ---------------------------------------------------------------
#     button_starti = pygame.image.load('picset/button/game_start2.png').convert_alpha() 
#     # button_start = pygame.transform.scale(button_start, (370, 120))
#     button_start = (1400, 700, button_starti, 370, 120)
#     button_start2 = button.Button(de_x/2-165,900, button_starti, 370, 120)
#     button_start3 = button.Button(de_x/2-(165*3),900, button_starti, 370, 120)
    
#     button_methodi = pygame.image.load('picset/button/method2.png').convert_alpha() 
#     # button_method = pygame.transform.scale(button_method, (370, 120))
#     button_method = button.Button(1400, 840, button_methodi, 370, 120)
    
#     button_reresti = pygame.image.load('picset/button/re_rest2.png').convert_alpha() 
#     # button_rerest = pygame.transform.scale(button_rerest, (370, 120))
#     button_rerest = button.Button(de_x/2+165,900, button_reresti, 370, 120)
    
#     button_restarti = pygame.image.load('picset/button/re_start2.png').convert_alpha() 
#     # button_restart = pygame.transform.scale(button_restart, (370, 120))
#     button_restart = button.Button(de_x*0.5-185, de_y*0.64, button_restarti, 370, 120)
#     button_restart2 = button.Button(580,830, button_restarti, 370, 120)
    
#     button_resumei = pygame.image.load('picset/button/resume2.png').convert_alpha() 
#     # button_resume = pygame.transform.scale(button_resume, (370, 120))
#     button_resume = button.Button(de_x*0.5-185, de_y*0.77, button_resumei, 370, 120)
    
#     button_jstarti = pygame.image.load('picset/button/start2.png').convert_alpha() 
#     # button_jstart = pygame.transform.scale(button_jstart, (370, 120))
#     button_jstart = button.Button(de_x/2-165,900, button_jstarti, 370, 120)
    
#     button_maini = pygame.image.load('picset/button/main2.png').convert_alpha() 
#     # button_main = pygame.transform.scale(button_main, (370, 120))
#     button_main = button.Button(de_x*0.5-185, de_y*0.51, button_maini, 370, 120)
#     button_main2 = button.Button(130,830, button_maini, 370, 120)
    
#     button_pausei = pygame.image.load('picset/button/pause2.png').convert_alpha() 
#     # button_pause = pygame.transform.scale(button_pause, (70, 70))
#     button_pause = button.Button(de_x*0.94, 40, button_pausei, 70, 70)
    
    
#     # button_left = button.Button(de_x*0.06, de_y-200, button_pausei, 70, 70)
#     button_right = button.Button(de_x*0.94, de_y-200, button_pausei, 70, 70)
    
#     button_left = button.Button(de_x*0.94-100, de_y-200, button_pausei, 70, 70)
#     button_up = button.Button(de_x*0.94-50, de_y-250, button_pausei, 70, 70)
#     button_down = button.Button(de_x*0.94-50, de_y-150, button_pausei, 70, 70)
    
    
#     button_testi = pygame.image.load('picset/button/test_start.png').convert_alpha() 
#     button_test = button.Button(de_x*0.94, de_y-350, button_testi, 70, 70)
    
#     # -------------- word ---------------------------------------------------------------
#     title_gold = pygame.image.load('picset/title_gold.png').convert_alpha() 
#     title_gold = pygame.transform.scale(title_gold, (900, 450))
#     title_word = pygame.image.load('picset/title_word.png').convert_alpha() 
#     title_word = pygame.transform.scale(title_word, (580, 290))
    
    
    
#     rest_title = pygame.image.load('picset/resting/resting_title.png').convert_alpha() 
#     rest_title = pygame.transform.scale(rest_title, (1000, 250))
    
#     pause_title = pygame.image.load('picset/object/pause.png').convert_alpha() 
#     pause_title = pygame.transform.scale(pause_title, (550, 150))
    
    
#     method = pygame.image.load('picset/method/method.jpg').convert_alpha() 
#     method = pygame.transform.scale(method, (1500, 750))
    
    
#     rest_ins = pygame.image.load('picset/resting/resting_start.png').convert_alpha() 
#     rest_ins = pygame.transform.scale(rest_ins, (1600, 400))
    
#     rest_expl = pygame.image.load('picset/resting/expl.png')
#     rest_expl = pygame.transform.scale(rest_expl, (de_x*0.9, de_y*0.9))
    
#     rest_rep = pygame.image.load('picset/resting/resting_report.png').convert_alpha() 
#     rest_rep = pygame.transform.scale(rest_rep, (1000, 250))
    
    
    
#     game_ready = pygame.image.load('picset/object/ready.png').convert_alpha() 
#     game_ready = pygame.transform.scale(game_ready, (600, 150))
    
#     game_start = pygame.image.load('picset/object/start.png').convert_alpha() 
#     game_start = pygame.transform.scale(game_start, (600, 150))
    
#     game_clear = pygame.image.load('picset/object/clear.png').convert_alpha() 
#     game_clear = pygame.transform.scale(game_clear, (1100, 200))
    
    
    
#     game_pauseb = pygame.image.load('picset/pause2.png').convert_alpha() 
#     game_pauseb = pygame.transform.scale(game_pauseb, (de_x*0.95, de_y*0.9))
    
    
    
#     # -------------- object ---------------------------------------------------------------
#     game_rock = pygame.image.load('picset/object/rock2.png').convert_alpha() 
#     game_rock = pygame.transform.scale(game_rock, (900, 800))
    
#     game_dia = pygame.image.load('picset/object/diamond.png').convert_alpha() 
#     game_dia = pygame.transform.scale(game_dia, (200, 200))
    
#     game_gold = pygame.image.load('picset/object/gold.png').convert_alpha() 
#     game_gold = pygame.transform.scale(game_gold, (200, 200))
    
    
    
    
#     game_stat1 = pygame.image.load('picset/status/bar1.png').convert_alpha() 
#     game_stat1 = pygame.transform.scale(game_stat1, (595, 70))
    
#     game_stat2 = pygame.image.load('picset/status/bar2.png').convert_alpha() 
#     game_stat2 = pygame.transform.scale(game_stat2, (595, 70))
    
#     game_stat3 = pygame.image.load('picset/status/bar3.png').convert_alpha() 
#     game_stat3 = pygame.transform.scale(game_stat3, (595, 70))
    
#     game_stat4 = pygame.image.load('picset/status/bar4.png').convert_alpha() 
#     game_stat4 = pygame.transform.scale(game_stat4, (595, 70))
    
#     game_stat5 = pygame.image.load('picset/status/bar5.png').convert_alpha() 
#     game_stat5 = pygame.transform.scale(game_stat5, (595, 70))
    
#     game_stbar = pygame.image.load('picset/status/bar_stat.png').convert_alpha() 
#     game_stbar = pygame.transform.scale(game_stbar, (15, 90))
    
#     game_stat = [game_stat1, game_stat2, game_stat3, game_stat4, game_stat5]
    
    
    
    
    
#     game_cl_b = pygame.image.load('picset/result_2.png').convert_alpha() 
#     game_cl_b = pygame.transform.scale(game_cl_b, (de_x*0.95, de_y*0.9))
    
#     game_cl_res = pygame.image.load('picset/result.png').convert_alpha() 
#     game_cl_res = pygame.transform.scale(game_cl_res, (923, 445))
    
#     game_cl_dia = pygame.image.load('picset/object/cl_dia.png').convert_alpha() 
#     game_cl_dia = pygame.transform.scale(game_cl_dia, (1000, 250))
    
#     game_cl_gold = pygame.image.load('picset/object/cl_gold.png').convert_alpha() 
#     game_cl_gold = pygame.transform.scale(game_cl_gold, (1000, 250))
    
    
    
    
    
    
#     eye_1 = pygame.image.load('picset/resting/eye11.png').convert_alpha() 
#     eye_1 = pygame.transform.scale(eye_1, (1600, 560))
    
#     eye_2 = pygame.image.load('picset/resting/eye2.png').convert_alpha() 
#     eye_2 = pygame.transform.scale(eye_2, (1600, 480))
    
#     eye_3 = pygame.image.load('picset/resting/eye3.png').convert_alpha() 
#     eye_3 = pygame.transform.scale(eye_3, (1600, 400))
    
#     rest_eye = [eye_1, eye_2, eye_3]
#     rest_eye_loc = [(de_x/2-800,de_y/2-220), (de_x/2-800,de_y/2-200), (de_x/2-800,de_y/2-30) ]
    
    
#     miner_intro = pygame.image.load('picset/character/miner_intro.png').convert_alpha() 
#     miner_intro = pygame.transform.scale(miner_intro, (700, 800))
    
    
    
#     miner_1 = pygame.image.load('picset/character/miner_1.png').convert_alpha() 
#     miner_1 = pygame.transform.scale(miner_1, (800, 850))
    
#     miner_2 = pygame.image.load('picset/character/miner_2.png').convert_alpha() 
#     miner_2 = pygame.transform.scale(miner_2, (800, 850))
    
#     miner_3 = pygame.image.load('picset/character/miner_3.png').convert_alpha() 
#     miner_3 = pygame.transform.scale(miner_3, (800, 850))
    
#     miner_4 = pygame.image.load('picset/character/miner_4.png').convert_alpha() 
#     miner_4 = pygame.transform.scale(miner_4, (800, 850))
    
#     miner_5 = pygame.image.load('picset/character/miner_5.png').convert_alpha() 
#     miner_5 = pygame.transform.scale(miner_5, (800, 850))
    
#     miner_6 = pygame.image.load('picset/character/miner_6.png').convert_alpha() 
#     miner_6 = pygame.transform.scale(miner_6, (800, 850))
    
    
#     miner_ani_set = [miner_1, miner_2, miner_3, miner_4, miner_5, miner_6]
#     miner_ani_loc = (de_x/2-270,de_y-850)
#     miner_rock_loc = [(de_x-600, de_y-600), (de_x-600+2, de_y-600+4)]
    
    
    
#     miner_rest = pygame.image.load('picset/character/miner_rest.png').convert_alpha() 
#     miner_rest = pygame.transform.scale(miner_rest, (780, 850))
    
#     miner_tired = pygame.image.load('picset/character/miner_tired2.png').convert_alpha() 
#     miner_tired = pygame.transform.scale(miner_tired, (780, 850))
    
#     miner_very = pygame.image.load('picset/character/miner_very.png').convert_alpha() 
#     miner_very = pygame.transform.scale(miner_very, (780, 850))
    
    
    
#     cart_full = pygame.image.load('picset/cart/cart_2.png').convert_alpha() 
#     cart_full = pygame.transform.scale(cart_full, (600, 600))
    
#     cart_half = pygame.image.load('picset/cart/cart_1.png').convert_alpha() 
#     cart_half = pygame.transform.scale(cart_half, (600, 600))
    
#     cart_empty = pygame.image.load('picset/cart/cart_0.png').convert_alpha() 
#     cart_empty = pygame.transform.scale(cart_empty, (600, 600))
    
#     cart_intro = pygame.transform.scale(cart_full, (600, 600))
    
#     cart_result = pygame.transform.scale(cart_full, (500, 500))