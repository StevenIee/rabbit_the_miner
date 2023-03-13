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


class resting_eye(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        
        size = (1600, 560)
        
        images = []
        images.append(pygame.image.load('IMAGES/picset/resting/eye1.png'))
        images.append(pygame.image.load('IMAGES/picset/resting/eye2.png'))
        images.append(pygame.image.load('IMAGES/picset/resting/eye3.png'))
        
        self.rect = pygame.Rect(position, size)
        
        self.images = [pygame.transform.scale(image, size) for image in images]
        
        self.index = 0
        self.image = images[self.index]
        
        self.animation_time = round(100 / len(self.images * 100), 2)
        self.current_time = 0
        
        
                      
    def update(self, mt):
        # self.index += 1
        self.current_time += mt
        
        # if restart:
        #     self.index = 0
        #     restart = False
        
        if self.current_time >= self.animation_time:
            self.current_time = 0
   
            self.index += 1
        if self.index >= len(self.images):
            self.index = len(self.images)-1

        self.image = self.images[self.index]
    
        
        # if self.index >= len(self.images):
        #     self.index = len(self.images)-1
        
        # self.image = self.images[self.index]


# def resting_eye_stop(screen, all_sprites):
#     all_sprites.draw(screen)

def resting_eye_play(screen, all_sprites, mt):
    all_sprites.update(mt)
    all_sprites.draw(screen)




def button_img():
    button_starti = pygame.image.load('IMAGES/picset/button/game_start2.png').convert_alpha() 
    button_methodi = pygame.image.load('IMAGES/picset/button/method2.png').convert_alpha() 
    button_reresti = pygame.image.load('IMAGES/picset/button/re_rest2.png').convert_alpha() 
    button_restarti = pygame.image.load('IMAGES/picset/button/re_start2.png').convert_alpha() 
    button_resumei = pygame.image.load('IMAGES/picset/button/resume2.png').convert_alpha() 
    button_jstarti = pygame.image.load('IMAGES/picset/button/start2.png').convert_alpha() 
    button_maini = pygame.image.load('IMAGES/picset/button/main2.png').convert_alpha() 
    button_pausei = pygame.image.load('IMAGES/picset/button/pause2.png').convert_alpha() 
    button_testi = pygame.image.load('IMAGES/picset/button/test_start.png').convert_alpha() 
    return button_starti, button_methodi, button_reresti, button_restarti, button_resumei, button_jstarti, button_maini, button_pausei, button_testi

def back_img(de_x, de_y):
    background_img = pygame.image.load('IMAGES/picset/background.jpg').convert_alpha() 
    background_img = pygame.transform.scale(background_img, (de_x, de_y))
    
    method_back = pygame.image.load('IMAGES/picset/method/background.jpg').convert_alpha() 
    method_back = pygame.transform.scale(method_back, (de_x, de_y))

    resting_back = pygame.image.load('IMAGES/picset/resting/resting_back.jpg').convert_alpha() 
    resting_back = pygame.transform.scale(resting_back, (de_x, de_y))
    
    game_back = pygame.image.load('IMAGES/picset/background_22.jpg').convert_alpha() 
    game_back = pygame.transform.scale(game_back, (de_x, de_y))

    
    title_gold = pygame.image.load('IMAGES/picset/title_gold.png').convert_alpha() 
    title_gold = pygame.transform.scale(title_gold, (900, 450))
    
    title_word = pygame.image.load('IMAGES/picset/title_word.png').convert_alpha() 
    title_word = pygame.transform.scale(title_word, (580, 290))
    
    rest_title = pygame.image.load('IMAGES/picset/resting/resting_title.png').convert_alpha() 
    rest_title = pygame.transform.scale(rest_title, (1000, 250))
    
    pause_title = pygame.image.load('IMAGES/picset/object/pause.png').convert_alpha() 
    pause_title = pygame.transform.scale(pause_title, (550, 150))
    
    
    method = pygame.image.load('IMAGES/picset/method/method.jpg').convert_alpha() 
    method = pygame.transform.scale(method, (1500, 750))
    
    rest_ins = pygame.image.load('IMAGES/picset/resting/resting_start.png').convert_alpha() 
    rest_ins = pygame.transform.scale(rest_ins, (1600, 400))
    
    rest_expl = pygame.image.load('IMAGES/picset/resting/expl.png')
    rest_expl = pygame.transform.scale(rest_expl, (de_x*0.9, de_y*0.9))
    
    rest_rep = pygame.image.load('IMAGES/picset/resting/resting_report.png').convert_alpha() 
    rest_rep = pygame.transform.scale(rest_rep, (1000, 250))
    
    game_pauseb = pygame.image.load('picset/pause2.png').convert_alpha() 
    game_pauseb = pygame.transform.scale(game_pauseb, (de_x*0.95, de_y*0.9))



    return background_img, method_back, resting_back, game_back, title_gold, title_word, rest_title, pause_title, method, rest_ins, rest_expl, rest_rep, game_pauseb

def miner_img():
    miner_intro = pygame.image.load('IMAGES/picset/character/miner_intro.png').convert_alpha() 
    miner_intro = pygame.transform.scale(miner_intro, (700, 800))
    return miner_intro

def cart_img():
    cart_full = pygame.image.load('IMAGES/picset/cart/cart_2.png').convert_alpha() 
    cart_full = pygame.transform.scale(cart_full, (600, 600))
    return cart_full



class gaming_ani(pygame.sprite.Sprite):
    def __init__(self, de_x, de_y):
        super().__init__()
        
        miner_size = (1600, 560)
        miner_position = (de_x/2-400,de_y-875)
        
        miner_images = []
        miner_images.append(pygame.image.load('IMAGES/picset/character/miner_1.png'))
        miner_images.append(pygame.image.load('IMAGES/picset/character/miner_2.png'))
        miner_images.append(pygame.image.load('IMAGES/picset/character/miner_3.png'))
        miner_images.append(pygame.image.load('IMAGES/picset/character/miner_4.png'))
        miner_images.append(pygame.image.load('IMAGES/picset/character/miner_5.png'))
        miner_images.append(pygame.image.load('IMAGES/picset/character/miner_6.png'))
        
        
        
        self.miner_rect = pygame.Rect(miner_position, miner_size)
        
        self.miner_images = [pygame.transform.scale(miner_image, miner_size) for miner_image in miner_images]
        
        self.miner_index = 0
        self.miner_image = miner_images[self.miner_index]
        
        self.animation_time = round(100 / len(self.miner_images * 100), 2)
        self.current_time = 0
        
        
        # stat_size = 
        # stat_bar = 
        
        
        # stat_images = []
        
        cart_size = (600, 600)
        cart_position = (de_x/2-950, de_y-625)
        
        cart_images = []
        cart_images.append(pygame.image.load('IMAGES/picset/cart/cart_0.png'))
        cart_images.append(pygame.image.load('IMAGES/picset/cart/cart_1.png'))
        cart_images.append(pygame.image.load('IMAGES/picset/cart/cart_2.png'))
        
        
        
        
        
                      
    def miner_update(self, mt):
        # self.index += 1
        self.current_time += mt
        
        # if restart:
        #     self.index = 0
        #     restart = False
        
        if self.current_time >= self.animation_time:
            self.current_time = 0
   
            self.miner_index += 1
        if self.miner_index >= len(self.miner_images):
            self.miner_index = len(self.miner_images)-1

        self.miner_image = self.miner_images[self.miner_index]



    def update(self, ):

        self.index += 1

 

        if self.index >= len(self.images):
            self.index = 0

        self.image = self.images[self.index]