# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 16:25:44 2023

@author: JISU
"""

import pygame
import math
import random


class Button:  # button class
    def __init__(self, x, y, image, width, height):
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()
        touch = False
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            touch = True
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
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

    return button_starti, button_methodi, button_reresti,\
           button_restarti, button_resumei, button_jstarti, \
           button_maini, button_pausei, button_testi


def back_img(de_x, de_y):
    background_img = pygame.image.load('IMAGES/picset/background.jpg').convert_alpha() 
    game_back = pygame.image.load('IMAGES/picset/background_22.jpg').convert_alpha()

    title_gold = pygame.image.load('IMAGES/picset/title_gold.png').convert_alpha() 
    title_gold = pygame.transform.scale(title_gold, (900, 440))
    
    title_word = pygame.image.load('IMAGES/picset/title_word.png').convert_alpha() 
    title_word = pygame.transform.scale(title_word, (580, 232))
    
    rest_title = pygame.image.load('IMAGES/picset/resting/resting_title.png').convert_alpha() 
    rest_title = pygame.transform.scale(rest_title, (1000, 250))
    
    pause_title = pygame.image.load('IMAGES/picset/object/pause.png').convert_alpha() 
    pause_title = pygame.transform.scale(pause_title, (550, 150))
    
    method = pygame.image.load('IMAGES/picset/method/method.jpg').convert_alpha()
    method_back = pygame.image.load('IMAGES/picset/method/background.jpg').convert_alpha()

    resting_back = pygame.image.load('IMAGES/picset/resting/resting_back.jpg').convert_alpha()
    rest_ins = pygame.image.load('IMAGES/picset/resting/resting_start.png').convert_alpha()
    rest_ins = pygame.transform.scale(rest_ins, (1600, 400))
    
    rest_expl = pygame.image.load('IMAGES/picset/resting/expl.png')
    rest_expl = pygame.transform.scale(rest_expl, (de_x*0.9, de_y*0.9))
    
    rest_rep = pygame.image.load('IMAGES/picset/resting/resting_report.png').convert_alpha() 
    rest_rep = pygame.transform.scale(rest_rep, (1000, 250))
    
    game_pauseb = pygame.image.load('IMAGES/picset/pause2.png').convert_alpha() 
    game_pauseb = pygame.transform.scale(game_pauseb, (de_x*0.95, de_y*0.9))
    
    game_cl_b = pygame.image.load('IMAGES/picset/result_2.png').convert_alpha() 
    game_cl_b = pygame.transform.scale(game_cl_b, (de_x*0.95, de_y*0.9))
    
    game_cl_res = pygame.image.load('IMAGES/picset/result.png').convert_alpha() 
    game_cl_res = pygame.transform.scale(game_cl_res, (923, 445))
    
    game_clear = pygame.image.load('IMAGES/picset/object/clear.png').convert_alpha() 
    game_clear = pygame.transform.scale(game_clear, (1100, 200))

    return background_img, method_back, resting_back, game_back, title_gold, title_word, rest_title, pause_title, method, rest_ins, rest_expl, rest_rep, game_pauseb, game_cl_b, game_cl_res, game_clear


def miner_img():
    miner_intro = pygame.image.load('IMAGES/picset/character/miner_intro.png').convert_alpha() 
    miner_intro = pygame.transform.scale(miner_intro, (700, 800))
    return miner_intro


def cart_img():
    cart_full = pygame.image.load('IMAGES/picset/cart/cart_2.png').convert_alpha() 
    cart_full = pygame.transform.scale(cart_full, (600, 600))
    return cart_full


def gaming_img():
    
    # Status Bar Images
    game_stat1 = pygame.image.load('IMAGES/picset/status/bar1.png').convert_alpha()  # 상태바1
    game_stat2 = pygame.image.load('IMAGES/picset/status/bar2.png').convert_alpha()  # 상태바2
    game_stat3 = pygame.image.load('IMAGES/picset/status/bar3.png').convert_alpha()  # 상태바3
    game_stat4 = pygame.image.load('IMAGES/picset/status/bar4.png').convert_alpha()  # 상태바4
    game_stat5 = pygame.image.load('IMAGES/picset/status/bar5.png').convert_alpha()  # 상태바5
    game_stbar = pygame.image.load('IMAGES/picset/status/bar_stat.png').convert_alpha()  # 상태 세로 게이지 바
    game_stat = [game_stat1, game_stat2, game_stat3, game_stat4, game_stat5]

    # Cart images
    cart_full = pygame.image.load('IMAGES/picset/cart/cart_2.png').convert_alpha()   # full cart
    cart_half = pygame.image.load('IMAGES/picset/cart/cart_1.png').convert_alpha()   # half_full cart
    cart_empty = pygame.image.load('IMAGES/picset/cart/cart_0.png').convert_alpha()  # emtpy cart
    cart_group = [cart_empty, cart_half, cart_full]

    # Miners
    miner_rest = pygame.image.load('IMAGES/picset/character/miner_rest.png').convert_alpha()  # miner size는 780 X 840
    miner_tired = pygame.image.load('IMAGES/picset/character/miner_tired2.png').convert_alpha()
    miner_very = pygame.image.load('IMAGES/picset/character/miner_very.png').convert_alpha()
    miner_set = [miner_very, miner_tired, miner_rest]

    # Minerals
    game_rock = pygame.image.load('IMAGES/picset/object/rock2.png').convert_alpha() 
    game_rock = pygame.transform.scale(game_rock, (900, 800))

    game_dia = pygame.image.load('IMAGES/picset/object/diamond.png').convert_alpha() 
    game_dia = pygame.transform.scale(game_dia, (200, 200))
    
    game_gold = pygame.image.load('IMAGES/picset/object/gold.png').convert_alpha() 
    game_gold = pygame.transform.scale(game_gold, (200, 200))
    
    game_reward = [game_gold, game_dia]
    
    return game_stat, game_stbar, cart_group, miner_set, game_rock, game_reward


# class gaming_ani(pygame.sprite.Sprite):
#     def __init__(self, de_x, de_y):
#         super().__init__()
        
#         miner_size = (1600, 560)
#         miner_position = (de_x/2-400,de_y-875)
        
#         miner_images = []
#         miner_images.append(pygame.image.load('IMAGES/picset/character/miner_1.png'))
#         miner_images.append(pygame.image.load('IMAGES/picset/character/miner_2.png'))
#         miner_images.append(pygame.image.load('IMAGES/picset/character/miner_3.png'))
#         miner_images.append(pygame.image.load('IMAGES/picset/character/miner_4.png'))
#         miner_images.append(pygame.image.load('IMAGES/picset/character/miner_5.png'))
#         miner_images.append(pygame.image.load('IMAGES/picset/character/miner_6.png'))
        
        
        
#         self.miner_rect = pygame.Rect(miner_position, miner_size)
        
#         self.miner_images = [pygame.transform.scale(miner_image, miner_size) for miner_image in miner_images]
        
#         self.miner_index = 0
#         self.miner_image = miner_images[self.miner_index]
        
#         self.animation_time = round(100 / len(self.miner_images * 100), 2)
#         self.current_time = 0
        
        
        
#         cart_size = (600, 600)
#         cart_positions = []
#         cart_positions.append((de_x/2-950, de_y-625))
#         cart_positions.append((de_x/2-950, de_y-627))
        
#         cart_images = []
#         cart_images.append(pygame.image.load('IMAGES/picset/cart/cart_0.png'))
#         cart_images.append(pygame.image.load('IMAGES/picset/cart/cart_1.png'))
#         cart_images.append(pygame.image.load('IMAGES/picset/cart/cart_2.png'))
        
        
#         self.cart_rect = pygame.Rect(cart_positions[0], cart_size) # 밑에서 조절하기!
        
#         self.cart_images = [pygame.transform.scale(cart_image, cart_size) for cart_image in cart_images]
        
#         self.cart_index = 0
#         self.cart_image = cart_images[self.cart_index]
        
        
#         rock_size = (900,800)
#         rock_positions = []
#         rock_positions.append((de_x-600, de_y-600))
#         rock_positions.append((de_x-600+2, de_y-600+4))
        
#         self.rock_image = pygame.image.load('IMAGES/picset/cart/cart_0.png')
        
#         self.rock_rect = pygame.Rect(rock_positions[0], rock_size) # 밑에서 조절해야함
#         # self.rock_image = [p]
        
#         stat_size = (595,70)
#         stat_position = (de_x*0.5-297.5, 50)
        
#         stat_images = []
#         stat_images.append(pygame.image.load('IMAGES/picset/status/bar1.png'))
#         stat_images.append(pygame.image.load('IMAGES/picset/status/bar2.png'))
#         stat_images.append(pygame.image.load('IMAGES/picset/status/bar3.png'))
#         stat_images.append(pygame.image.load('IMAGES/picset/status/bar4.png'))
#         stat_images.append(pygame.image.load('IMAGES/picset/status/bar5.png'))
        
#         self.stat_rect = pygame.Rect(stat_position, stat_size)
#         self.stat_images = [pygame.transform.scale(stat_image, stat_size) for stat_image in stat_images]
        
#         self.stat_index = 0 # 이걸 밑에서 조절해야함
        
        
#         reward_size = (2,2)
#         reward_position = (2,2)
        
#         reward_images = []
#         reward_images.append(pygame.image.load('IMAGES/picset/object/gold.png'))
#         reward_images.append(pygame.image.load('IMAGES/picset/object/diamond.png'))
        
#         self.reward_rect = pygame.Rect(reward_position, reward_size)
#         self.reward_images = [pygame.transform.scale(stat_image, stat_size) for stat_image in stat_images]
        
#         self.reward_index = 0 # 이걸 밑에서 조절해야함
        
                      
#     def miner_update(self, mt):
#         # self.index += 1
#         self.current_time += mt
        
#         # if restart:
#         #     self.index = 0
#         #     restart = False
        
#         if self.current_time >= self.animation_time:
#             self.current_time = 0
   
#             self.miner_index += 1
#         if self.miner_index >= len(self.miner_images):
#             self.miner_index = len(self.miner_images)-1

#         self.miner_image = self.miner_images[self.miner_index]



#     def reward_update(self):
#         reward_position = (1,2)



#     def stat_color(self, game_bound):
#         self.stat_image = self.stat_images[game_bound]



class miner_animation(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        size = (780, 840)
        position = (690, 230)  # (560.0, 205) # de_x, de_y로 안해서 나중에 만약 해상도 바꾸면 건드려야 함 (de_x/2-400,de_y-875)
        # ani_stop = False
        images = []
        images.append(pygame.image.load('IMAGES/picset/character/miner_1.png'))
        images.append(pygame.image.load('IMAGES/picset/character/miner_2.png'))
        images.append(pygame.image.load('IMAGES/picset/character/miner_3.png'))
        images.append(pygame.image.load('IMAGES/picset/character/miner_4.png'))
        images.append(pygame.image.load('IMAGES/picset/character/miner_5.png'))
        images.append(pygame.image.load('IMAGES/picset/character/miner_6.png'))
        images.append(pygame.image.load('IMAGES/picset/character/miner_1.png'))
        
        self.rect = pygame.Rect(position, size)

        # rect size is same as picture image size
        self.images = images
        # self.images = [pygame.transform.scale(image, size) for image in images]
        
        self.index = 0
        self.image = images[self.index]
        
        # self.animation_time = round(100 / len(self.images * 100), 2)
        self.current_time = 0
        self.animation_time = self.animation_time = round(100 / len(self.images * 100), 2)
        
                      
    def update(self, mt):
        
        self.current_time += mt
        
        if self.current_time >= self.animation_time:
            self.current_time = 0
   
            self.index += 1
        if self.index >= len(self.images):
            self.index = len(self.images)-1

        self.image = self.images[self.index]
        
        # init_rock = False
        # ani_stop = False
        
        # if self.index == 4:
        #     init_rock = True
        #     ani_stop = False
        # elif self.index == 6:
        #     ani_stop = True
        # else:
        #     init_rock = False
        #     ani_stop = False
        
        # rock_ani = [init_rock, ani_stop]
        
        index_num = self.index
        return index_num
        # return init_rock, ani_stop#rock_ani#init_rock, ani_stop
        
            
        
    
    # def animation_control(self, ani_init):
    #     if ani_init == 3:
    #         self.animation_time = self.animation_time = round(100 / len(self.images * 100), 2)
    #     elif ani_init == 4:
    #         self.animation_time = self.animation_time = round(100 / len(self.images * 150), 2)


def miner_ani_starter(screen, miner_sprite, ani_init, mt, game_rock, de_x, de_y, draw_reward, cart_group, cart_num, ani_frame):
    index_num = miner_sprite.update(mt)
    
    if index_num == 4:
        init_rock = True
        ani_stop = False
    elif index_num == 6:
        ani_stop = True
    else:
        init_rock = False
        ani_stop = False
    
    # miner_sprite.animation_control(ani_init)
    # init_rock, ani_stop
    # rock_ani = miner_sprite.update(mt)
    # init_rock, ani_stop = miner_sprite.update(mt)
    # print(rock_ani)
    # init_rock = rock_ani[0]
    # ani_stop = rock_ani[1]
    #rock 
    if init_rock == True:
        screen.blit(game_rock,(de_x-600, de_y-600))
        cr_st = False
        # ani_frame = 0
    else:
        screen.blit(game_rock,(de_x-600+2, de_y-600+4))
        cr_st = True
        # ani_frame = 0
    

    
    #miner
    miner_sprite.draw(screen)
    
    #cart & reward
    if cr_st == True:
        # reward 뭐가 나올지 지정
        # if reward_select == 1:
        #     draw_reward = game_reward[0]
        # elif reward_select == 2:
        #     draw_reward = game_reward[1]
            
        draw_cart = cart_group[cart_num]
        # reward rotate
        # draw_reward = pygame.transform.rotate(draw_reward, random.randint(1,4)*90)
        ani_frame = ani_frame + 1
        # ani_frame = cart_reward(screen, ani_frame, de_x, de_y, draw_reward, draw_cart)
        cart_reward(screen, ani_frame, de_x, de_y, draw_reward, draw_cart)
        
    if ani_stop:
        ani_start = False    
    else:
        ani_start = True        
    return ani_start, ani_frame


def cart_reward(screen, ani_frame, de_x, de_y, draw_reward, draw_cart):
    # ani_frame = ani_frame + 1
    vel = 380
    ang = 60
    
    y_ani_temp = vel*math.sin(math.radians(ang))*ani_frame

    
    x_ani = de_x-500 - vel*math.cos(math.radians(ang))*ani_frame*0.1
    y_ani = de_y-450 - (y_ani_temp - 5*(ani_frame**2))*0.1

    if y_ani < de_y-440:
        screen.blit(draw_reward, (x_ani, y_ani))
        cart_x = de_x/2-950
        cart_y = de_y-627
    else:
        # screen.blit(draw_reward, (x_ani, y_ani))
        cart_x = de_x/2-950
        cart_y = de_y-625
        
    screen.blit(draw_cart, (cart_x, cart_y))
    
    
    # return ani_frame

