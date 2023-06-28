# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 10:41:08 2023

@author: JISU
"""


#%% intro and button 



# import package
import pygame, os, math, random
from datetime import datetime
import numpy as np

import pandas as pd

# game file path & data path ===================================path 설정 필요
org_path = 'D:/DCNL/DTx/neurofeedback/rabbit_the_miner/rabbit_the_miner'
os.chdir(org_path) 

# my modules
import button_adjustment


# data path
data_path = org_path + '/data'

if not os.path.isdir(data_path):
    os.mkdir(data_path)



#%% get user data (not be used in here)


# version_name = '2023.02.01 demo version'
# version_name1 = '2023.02.01'
# version_name2 = 'demo version'
# print1 = '================================================================='

# print(print1)
# print(print1 + '\n')

# print('                      leelab Neurofeedback\n')

# print('                                          '+version_name +'\n')
# print('developed by Jisu Chung\n')

# print(print1+ '\n\n')

# print('Player Information')
# player_id = input('input your id : ')
# session_numi = input('input session number : ')


# session_num = int(session_numi)

# player_date_temp = datetime.now()
# player_date = player_date_temp.strftime('%Y_%m_%d')
# player_date2 = player_date_temp.strftime('%Y_%m_%d_%H%M%S')

# player_filename = 'Player_' + player_id + '_Session_' + session_numi + '_' + player_date2

# if session_num > 1:
#     print('\n\nWelcome Back!')


# print('\nloading....\n')



# # data file create 

# datafile_name = data_path+'/'+player_filename+'.csv'






# data_temp = {'ID': player_id, 'date': player_date, 'session': session_num}
# data_temp2 = pd.DataFrame.from_dict(data_temp, orient = 'index')

# player_data = data_temp2.transpose()

# player_data.to_csv(datafile_name)




#%% initial setting

# start pygame
pygame.init()

# 
pygame.display.set_caption("leelab_Neurofeedback")



#screen size setting

screen_size = (1920,1080)
screen = pygame.display.set_mode(screen_size)
#screen = pygame.display.set_mode()


# get screen size
de_x, de_y = screen.get_size()
print(de_x, de_y)






#%% images



# IMAGE
# call image
background_img = pygame.image.load('IMAGES/picset/background.jpg').convert_alpha() 
# transform image
background_img = pygame.transform.scale(background_img, (de_x, de_y))


method_back = pygame.image.load('IMAGES/picset/method/background.jpg').convert_alpha() 
method_back = pygame.transform.scale(method_back, (de_x, de_y))

resting_back = pygame.image.load('IMAGES/picset/resting/resting_back.jpg').convert_alpha() 
resting_back = pygame.transform.scale(resting_back, (de_x, de_y))

game_back = pygame.image.load('IMAGES/picset/background_22.jpg').convert_alpha() 
game_back = pygame.transform.scale(game_back, (de_x, de_y))



# -------------- Button ---------------------------------------------------------------
button_starti = pygame.image.load('IMAGES/picset/button/game_start2.png').convert_alpha() 
# button_start = pygame.transform.scale(button_start, (370, 120))
button_start = button_adjustment.Button(1400, 700, button_starti, 370, 120)
button_start2 = button_adjustment.Button(de_x/2-165,900, button_starti, 370, 120)
button_start3 = button_adjustment.Button(de_x/2-(165*3),900, button_starti, 370, 120)

button_methodi = pygame.image.load('IMAGES/picset/button/method2.png').convert_alpha() 
# button_method = pygame.transform.scale(button_method, (370, 120))
button_method = button_adjustment.Button(1400, 840, button_methodi, 370, 120)

button_reresti = pygame.image.load('IMAGES/picset/button/re_rest2.png').convert_alpha() 
# button_rerest = pygame.transform.scale(button_rerest, (370, 120))
button_rerest = button_adjustment.Button(de_x/2+165,900, button_reresti, 370, 120)

button_restarti = pygame.image.load('IMAGES/picset/button/re_start2.png').convert_alpha() 
# button_restart = pygame.transform.scale(button_restart, (370, 120))
button_restart = button_adjustment.Button(de_x*0.5-185, de_y*0.64, button_restarti, 370, 120)
button_restart2 = button_adjustment.Button(580,830, button_restarti, 370, 120)

button_resumei = pygame.image.load('IMAGES/picset/button/resume2.png').convert_alpha() 
# button_resume = pygame.transform.scale(button_resume, (370, 120))
button_resume = button_adjustment.Button(de_x*0.5-185, de_y*0.77, button_resumei, 370, 120)

button_jstarti = pygame.image.load('IMAGES/picset/button/start2.png').convert_alpha() 
# button_jstart = pygame.transform.scale(button_jstart, (370, 120))
button_jstart = button_adjustment.Button(de_x/2-165,900, button_jstarti, 370, 120)

button_maini = pygame.image.load('IMAGES/picset/button/main2.png').convert_alpha() 
# button_main = pygame.transform.scale(button_main, (370, 120))
button_main = button_adjustment.Button(de_x*0.5-185, de_y*0.51, button_maini, 370, 120)
button_main2 = button_adjustment.Button(130,830, button_maini, 370, 120)

button_pausei = pygame.image.load('IMAGES/picset/button/pause2.png').convert_alpha() 
# button_pause = pygame.transform.scale(button_pause, (70, 70))
button_pause = button_adjustment.Button(de_x*0.94, 40, button_pausei, 70, 70)


# button_left = button.Button(de_x*0.06, de_y-200, button_pausei, 70, 70)
button_right = button_adjustment.Button(de_x*0.94, de_y-200, button_pausei, 70, 70)

button_left = button_adjustment.Button(de_x*0.94-100, de_y-200, button_pausei, 70, 70)
button_up = button_adjustment.Button(de_x*0.94-50, de_y-250, button_pausei, 70, 70)
button_down = button_adjustment.Button(de_x*0.94-50, de_y-150, button_pausei, 70, 70)


button_testi = pygame.image.load('IMAGES/picset/button/test_start.png').convert_alpha() 
button_test = button_adjustment.Button(de_x*0.94, de_y-350, button_testi, 70, 70)






# -------------- word ---------------------------------------------------------------
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



game_ready = pygame.image.load('IMAGES/picset/object/ready.png').convert_alpha() 
game_ready = pygame.transform.scale(game_ready, (600, 150))

game_start = pygame.image.load('IMAGES/picset/object/start.png').convert_alpha() 
game_start = pygame.transform.scale(game_start, (600, 150))

game_clear = pygame.image.load('IMAGES/picset/object/clear.png').convert_alpha() 
game_clear = pygame.transform.scale(game_clear, (1100, 200))



game_pauseb = pygame.image.load('IMAGES/picset/pause2.png').convert_alpha() 
game_pauseb = pygame.transform.scale(game_pauseb, (de_x*0.95, de_y*0.9))



# -------------- object ---------------------------------------------------------------
game_rock = pygame.image.load('IMAGES/picset/object/rock2.png').convert_alpha() 
game_rock = pygame.transform.scale(game_rock, (900, 800))

game_dia = pygame.image.load('IMAGES/picset/object/diamond.png').convert_alpha() 
game_dia = pygame.transform.scale(game_dia, (200, 200))

game_gold = pygame.image.load('IMAGES/picset/object/gold.png').convert_alpha() 
game_gold = pygame.transform.scale(game_gold, (200, 200))




game_stat1 = pygame.image.load('IMAGES/picset/status/bar1.png').convert_alpha() 
game_stat1 = pygame.transform.scale(game_stat1, (595, 70))

game_stat2 = pygame.image.load('IMAGES/picset/status/bar2.png').convert_alpha() 
game_stat2 = pygame.transform.scale(game_stat2, (595, 70))

game_stat3 = pygame.image.load('IMAGES/picset/status/bar3.png').convert_alpha() 
game_stat3 = pygame.transform.scale(game_stat3, (595, 70))

game_stat4 = pygame.image.load('IMAGES/picset/status/bar4.png').convert_alpha() 
game_stat4 = pygame.transform.scale(game_stat4, (595, 70))

game_stat5 = pygame.image.load('IMAGES/picset/status/bar5.png').convert_alpha() 
game_stat5 = pygame.transform.scale(game_stat5, (595, 70))

game_stbar = pygame.image.load('IMAGES/picset/status/bar_stat.png').convert_alpha() 
game_stbar = pygame.transform.scale(game_stbar, (15, 90))

game_stat = [game_stat1, game_stat2, game_stat3, game_stat4, game_stat5]





game_cl_b = pygame.image.load('IMAGES/picset/result_2.png').convert_alpha() 
game_cl_b = pygame.transform.scale(game_cl_b, (de_x*0.95, de_y*0.9))

game_cl_res = pygame.image.load('IMAGES/picset/result.png').convert_alpha() 
game_cl_res = pygame.transform.scale(game_cl_res, (923, 445))

game_cl_dia = pygame.image.load('IMAGES/picset/object/cl_dia.png').convert_alpha() 
game_cl_dia = pygame.transform.scale(game_cl_dia, (1000, 250))

game_cl_gold = pygame.image.load('IMAGES/picset/object/cl_gold.png').convert_alpha() 
game_cl_gold = pygame.transform.scale(game_cl_gold, (1000, 250))






eye_1 = pygame.image.load('IMAGES/picset/resting/eye1.png').convert_alpha() 
eye_1 = pygame.transform.scale(eye_1, (1600, 560))

eye_2 = pygame.image.load('IMAGES/picset/resting/eye2.png').convert_alpha() 
eye_2 = pygame.transform.scale(eye_2, (1600, 480))

eye_3 = pygame.image.load('IMAGES/picset/resting/eye3.png').convert_alpha() 
eye_3 = pygame.transform.scale(eye_3, (1600, 400))

rest_eye = [eye_1, eye_2, eye_3]
rest_eye_loc = [(de_x/2-800,de_y/2-220), (de_x/2-800,de_y/2-200), (de_x/2-800,de_y/2-30) ]


miner_intro = pygame.image.load('IMAGES/picset/character/miner_intro.png').convert_alpha() 
miner_intro = pygame.transform.scale(miner_intro, (700, 800))



miner_1 = pygame.image.load('IMAGES/picset/character/miner_1.png').convert_alpha() 
miner_1 = pygame.transform.scale(miner_1, (800, 850))

miner_2 = pygame.image.load('IMAGES/picset/character/miner_2.png').convert_alpha() 
miner_2 = pygame.transform.scale(miner_2, (800, 850))

miner_3 = pygame.image.load('IMAGES/picset/character/miner_3.png').convert_alpha() 
miner_3 = pygame.transform.scale(miner_3, (800, 850))

miner_4 = pygame.image.load('IMAGES/picset/character/miner_4.png').convert_alpha() 
miner_4 = pygame.transform.scale(miner_4, (800, 850))

miner_5 = pygame.image.load('IMAGES/picset/character/miner_5.png').convert_alpha() 
miner_5 = pygame.transform.scale(miner_5, (800, 850))

miner_6 = pygame.image.load('IMAGES/picset/character/miner_6.png').convert_alpha() 
miner_6 = pygame.transform.scale(miner_6, (800, 850))


miner_ani_set = [miner_1, miner_2, miner_3, miner_4, miner_5, miner_6]
miner_ani_loc = (de_x/2-270,de_y-850)
miner_rock_loc = [(de_x-600, de_y-600), (de_x-600+2, de_y-600+4)]



miner_rest = pygame.image.load('IMAGES/picset/character/miner_rest.png').convert_alpha() 
miner_rest = pygame.transform.scale(miner_rest, (780, 850))

miner_tired = pygame.image.load('IMAGES/picset/character/miner_tired2.png').convert_alpha() 
miner_tired = pygame.transform.scale(miner_tired, (780, 850))

miner_very = pygame.image.load('IMAGES/picset/character/miner_very.png').convert_alpha() 
miner_very = pygame.transform.scale(miner_very, (780, 850))



cart_full = pygame.image.load('IMAGES/picset/cart/cart_2.png').convert_alpha() 
cart_full = pygame.transform.scale(cart_full, (600, 600))

cart_half = pygame.image.load('IMAGES/picset/cart/cart_1.png').convert_alpha() 
cart_half = pygame.transform.scale(cart_half, (600, 600))

cart_empty = pygame.image.load('IMAGES/picset/cart/cart_0.png').convert_alpha() 
cart_empty = pygame.transform.scale(cart_empty, (600, 600))

cart_intro = pygame.transform.scale(cart_full, (600, 600))

cart_result = pygame.transform.scale(cart_full, (500, 500))



# =========================================================================
# 여기에 필요한 사진들 넣고 크기 조정

button_returni = pygame.image.load('IMAGES/picset/button/test_return.png').convert_alpha() 
button_return = button_adjustment.Button(de_x*0.94, de_y-350, button_returni, 70, 70)  # 앞 숫자 - 위치 / 뒤 숫자 -크기




#%% screens


# words 
font6 = pygame.font.SysFont('arial',50, True)
for_start = font6.render('Press SPACE to start', False, 'White')
font_x, font_y = for_start.get_size()



def introscreen():
    screen.blit(background_img,(0,0))
    screen.blit(title_gold,(1050,40))
    screen.blit(title_word,(1200,50))
    screen.blit(miner_intro,(140,250))
    screen.blit(cart_intro,(750,450))
    

def method_scr():
    screen.blit(method_back,(0,0))
    screen.blit(method,((de_x-1400)/2,100))
    

def resting_met(): 
    screen.blit(resting_back,(0,0))    
    screen.blit(rest_expl,(de_x*0.05,de_y*0.07))
    screen.blit(rest_title,((de_x-1000)/2,50))


# will animate soon.....
def resting_scra():
    screen.blit(resting_back,(0,0))
    screen.blit(rest_ins,((de_x-1600)/2,50))
    # screen.blit(eye_1,(de_x/2-800,de_y/2-200))
    screen.blit(eye_1,(de_x/2-800,de_y/2-220)) # for eye11
    
def resting_scrb():
    screen.blit(resting_back,(0,0))
    screen.blit(rest_ins,((de_x-1600)/2,50))
    screen.blit(eye_2,(de_x/2-800,de_y/2-200))

def resting_scrc():
    screen.blit(resting_back,(0,0))
    screen.blit(rest_ins,((de_x-1600)/2,50))
    screen.blit(eye_3,(de_x/2-800,de_y/2-30))
    
    
    
    
def resting_scr():
    screen.blit(resting_back,(0,0))
    screen.blit(rest_ins,((de_x-1600)/2,50))
    # screen.blit(eye_3,(de_x/2-800,de_y/2-30))    
    


#
def resting_res():
    screen.blit(resting_back,(0,0))
    screen.blit(rest_rep,((de_x-1000)/2,70))
    # screen.blit(button_start,(de_x/2-(165*3),900))
    # screen.blit(button_rerest,(de_x/2+165,900))
    # button_start3.draw(screen)
    # button_rerest.draw(screen)



# also here!    
def gaming_rd():
    screen.blit(game_back,(0,0))
    screen.blit(game_rock,(de_x-600,de_y-600))
    screen.blit(miner_rest,(de_x/2-400,de_y-875))
    screen.blit(cart_empty,(de_x/2-950,de_y-625))
    screen.blit(game_ready,(de_x/2-900,de_y-800))
    
    
    
def gaming_st():
    screen.blit(game_back,(0,0))
    screen.blit(game_rock,(de_x-600,de_y-600))
    screen.blit(miner_rest,(de_x/2-400,de_y-875))
    screen.blit(cart_empty,(de_x/2-950,de_y-625))
    screen.blit(game_start,(de_x/2-900,de_y-800))


def gaming_mining():
    screen.blit(game_back,(0,0))
    # screen.blit(game_rock,(de_x-600, de_y-600))
    # screen.blit(miner_1,(de_x/2-270,de_y-850))
    screen.blit(cart_full,(de_x/2-950, de_y-625))
    # button_pause.draw(screen)
    screen.blit(game_stat4,(de_x*0.5-297.5, 50))
    screen.blit(game_stbar,(de_x*0.5-297.5-15+(595*.75), 50-7.5))
    


def gaming_a():
    screen.blit(game_back,(0,0))
    screen.blit(game_rock,(de_x-600, de_y-600))
    screen.blit(miner_1,(de_x/2-270,de_y-850))
    screen.blit(cart_empty,(de_x/2-950, de_y-625))
    # button_pause.draw(screen)
    screen.blit(game_stat4,(de_x*0.5-297.5, 50))
    
def gaming_b():
    screen.blit(game_back,(0,0))
    screen.blit(game_rock,(de_x-600, de_y-600))
    screen.blit(miner_2,(de_x/2-270,de_y-850))
    screen.blit(cart_empty,(de_x/2-950, de_y-625))
    # button_pause.draw(screen)
    screen.blit(game_stat4,(de_x*0.5-297.5, 50))
    
    
def gaming_c():
    screen.blit(game_back,(0,0))
    screen.blit(game_rock,(de_x-600, de_y-600))
    screen.blit(miner_3,(de_x/2-270,de_y-850))
    screen.blit(cart_empty,(de_x/2-950, de_y-625))
    # button_pause.draw(screen)
    screen.blit(game_stat4,(de_x*0.5-297.5, 50))
    
def gaming_d():
    screen.blit(game_back,(0,0))
    screen.blit(game_rock,(de_x-600, de_y-600))
    screen.blit(miner_4,(de_x/2-270,de_y-850))
    screen.blit(cart_empty,(de_x/2-950, de_y-625))
    # button_pause.draw(screen)
    screen.blit(game_stat4,(de_x*0.5-297.5, 50))
    
def gaming_e():
    screen.blit(game_back,(0,0))
    screen.blit(game_rock,(de_x-600, de_y-600))
    screen.blit(miner_5,(de_x/2-270,de_y-850))
    screen.blit(cart_empty,(de_x/2-950, de_y-625))
    # button_pause.draw(screen)
    screen.blit(game_stat4,(de_x*0.5-297.5, 50))
    
def gaming_f():
    screen.blit(game_back,(0,0))
    screen.blit(game_rock,(de_x-600, de_y-600))
    screen.blit(miner_6,(de_x/2-270,de_y-850))
    screen.blit(cart_empty,(de_x/2-950, de_y-625))
    # button_pause.draw(screen)
    screen.blit(game_stat4,(de_x*0.5-297.5, 50))



    
def gaming_tir():
    screen.blit(game_back,(0,0))
    screen.blit(game_rock,(de_x-600, de_y-600))
    screen.blit(miner_tired,(de_x/2-340, de_y-850))
    screen.blit(cart_empty,(de_x/2-950, de_y-625))
    # button_pause.draw(screen)
    screen.blit(game_stat2,(de_x*0.5-297.5, 50))
    screen.blit(game_stbar,(de_x*0.5-297.5-15+(595*.25), 50-7.5))
    
def gaming_vet():
    screen.blit(game_back,(0,0))
    screen.blit(game_rock,(de_x-600, de_y-600))
    screen.blit(miner_very,(de_x/2-400, de_y-875))
    screen.blit(cart_empty,(de_x/2-950, de_y-625))
    # button_pause.draw(screen)
    screen.blit(game_stat1,(de_x*0.5-297.5, 50))
    screen.blit(game_stbar,(de_x*0.5-297.5-15+(595*.1), 50-7.5))
    
    
def gaming_res():
    screen.blit(game_back,(0,0))
    screen.blit(game_rock,(de_x-600, de_y-600))
    screen.blit(miner_rest,(de_x/2-400,de_y-875))
    screen.blit(cart_empty,(de_x/2-950, de_y-625))
    # button_pause.draw(screen)
    screen.blit(game_stat3,(de_x*0.5-297.5, 50))
    screen.blit(game_stbar,(de_x*0.5-297.5-15+(595*.5), 50-7.5))
    
    




    
    
def gaming_pause():
    screen.blit(game_pauseb,(de_x*0.025,de_y*0.05))
    screen.blit(pause_title,(de_x*0.5-275, de_y*0.2))
    

    
# 여기 수정 하면 됨 230628 ==================================================
# 여기서 이미지 위치 조정 

def gaming_result():
    screen.blit(game_back,(0,0))
    screen.blit(game_cl_b,(de_x*0.025,de_y*0.05))
    screen.blit(game_cl_res,(de_x*0.025,de_y*0.5-200))
    screen.blit(cart_result,(de_x-930, de_y-750))
    screen.blit(miner_intro,(de_x-750, de_y-900))
    screen.blit(game_clear,(de_x*0.05, 120))


def session_result():
    screen.blit(game_back,(0,0))
    screen.blit(game_cl_b,(de_x*0.025,de_y*0.05))



def all_session():
    screen.blit(game_back,(0,0))
    screen.blit(game_cl_b,(de_x*0.025,de_y*0.05))


#%% start function


game_starter = False
# game_status = "intro"


# ========================================================== 무슨 화면 조정할지 선택
# game_status = "rest_start" # for animation (rest)
game_status = "game_result" # ''
# ==========================================================

miner_status = 0 # "

# miner_status = 0
miner_ani = 1
miner_animation = False # for animation
miner_frame_n = 10
miner_frame = 0
miner_num = 0

ani_frame = 0


rest_key = 1
rest_ani = False # for animation
rest_state = 0
rest_ani_buff = [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,2]
rest_ani_buff_len = len(rest_ani_buff)

game_paused = False

game_status_old = game_status
# clock - for game loop (fps)
clock= pygame.time.Clock()
run = True

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
        
        if keys_act[pygame.K_LEFT]:
            game_status = game_status_old
            
        
    screen.fill((100, 100, 110))
    
    if game_starter == True:
        
        if game_status == "intro":
            introscreen()
            if button_method.draw(screen):
                game_status_old = game_status
                game_status = "method"
                
            if button_start.draw(screen):
                game_status_old = game_status
                game_status = "rest_method"

        if game_status == "method":
            method_scr()
            if button_start2.draw(screen):
                game_status_old = game_status
                game_status = "rest_method"
                
        if game_status == "rest_method":
            resting_met()
            if button_jstart.draw(screen): 
                game_status_old = game_status
                game_status = "rest_start"
                
                
        if game_status == "rest_start": 
            resting_scr()
            
            if button_test.draw(screen):
                rest_ani = True
                rest_state = 0
                
            if rest_ani:
                if rest_state == rest_ani_buff_len-1:
                    rest_state = rest_ani_buff_len-1
                else:
                    rest_state = rest_state + 1
            
            resting_ani = rest_eye[rest_ani_buff[rest_state]]
            resting_loc = rest_eye_loc[rest_ani_buff[rest_state]]
            screen.blit(resting_ani, resting_loc)
            
                
            
                
            if keys_act[pygame.K_DOWN]: 
                game_status_old = game_status
                game_status = "rest_result" 
                

        if game_status == "rest_result":
            resting_res() 
            if button_start3.draw(screen):
                game_status_old = game_status
                game_status = "game_starting"
            if button_rerest.draw(screen):
                game_status_old = game_status
                game_status = "rest_method"
        
        if game_status == "game_starting":
            game_paused = False  
            gaming_rd()
            
            if button_right.draw(screen):
                game_status_old = game_status
                game_status = "game_starting2" 
        
        if game_status == "game_starting2":
            gaming_st()
            
            if button_right.draw(screen):
                game_status_old = game_status
                game_status = "game_start" 
        
        if game_status == "game_start":
            

            
            if miner_status == -2:
                gaming_vet()
                if button_pause.draw(screen):
                    game_paused = True                
                # if keys_act[pygame.K_UP]:
                if button_right.draw(screen):
                    miner_status = miner_status + 1
                if keys_act[pygame.K_KP_ENTER]:
                    game_status = "game_result"
                 
            
            elif miner_status == -1:
                gaming_tir()
                if button_pause.draw(screen):
                    game_paused = True                
                # if keys_act[pygame.K_UP]:
                if button_right.draw(screen):
                    miner_status = miner_status + 1
                # elif keys_act[pygame.K_DOWN]:
                if button_left.draw(screen):
                    miner_status = miner_status -1
                if keys_act[pygame.K_KP_ENTER]:
                    game_status = "game_result"

            
            elif miner_status == 0:
                gaming_res()
                if button_pause.draw(screen):
                    game_paused = True
                # if keys_act[pygame.K_UP]:
                if button_right.draw(screen):
                    miner_status = miner_status + 1
                # elif keys_act[pygame.K_DOWN]:
                if button_left.draw(screen):
                    miner_status = miner_status -1
                if keys_act[pygame.K_KP_ENTER]:
                    game_status = "game_result"

                
            elif miner_status == 1:
                gaming_mining()
                # ani_frame = 0
                if miner_animation:
                    if miner_frame == miner_frame_n:
                        miner_frame = 0
                        if miner_num == 5:
                            miner_num = 0
                        else:
                            miner_num = miner_num + 1
                    else:
                        miner_frame = miner_frame + 1
                    

                
                if miner_num == 4:
                    rock_loc = miner_rock_loc[1]
                else:
                    rock_loc = miner_rock_loc[0]
                
                
                miner_ani_img = miner_ani_set[miner_num]
                
                screen.blit(game_rock, rock_loc)
                screen.blit(miner_ani_img, miner_ani_loc)

                if button_test.draw(screen):
                    miner_animation = True
                    miner_num = 0
                    miner_frame = 0
                    ani_frame = 0
                    game_dia = pygame.transform.rotate(game_dia, random.randint(1,4)*90)
                    x_ani = de_x-500
                    y_ani = de_y-450
                    
                if button_pause.draw(screen):
                    game_paused = True          
                    
                if button_left.draw(screen):
                    miner_status = miner_status -1
                    
                if keys_act[pygame.K_KP_ENTER]:
                    game_status = "game_result"
                    
                    
                # x_ani = []
                # y_ani = []
                # x_ani = 0
                # y_ani = 0
                    
                screen.blit(game_dia, (de_x-500, de_y-450))
                # screen.blit(game_dia, (de_x-600, de_y-600))
                
                ani = list(np.arange(0,10))
                ani_frame = ani_frame + 1
                # for i in ani:
                    
                #     x_ani[i] = de_x-500 - 36*math.cos(math.radians(56))*ani_frame
                #     y_ani[i] = de_y-450 - 36*math.cos(math.radians(56))*ani_frame
                    
                #     screen.blit(game_dia, (x_ani[i], y_ani[i]))
                vel = 380
                ang = 60
                
                y_ani_temp = vel*math.sin(math.radians(ang))*ani_frame

                
                x_ani = de_x-500 - vel*math.cos(math.radians(ang))*ani_frame*0.1
                y_ani = de_y-450 - (y_ani_temp - 5*(ani_frame**2))*0.1
                
                if y_ani == de_y-440:
                    screen.blit(game_dia, (x_ani, y_ani))
                else:
                    screen.blit(game_dia, (x_ani, y_ani))
                
                # game_dia = pygame.transform.rotate(game_dia, ani_frame*0.1)
                
                
                
                screen.blit(game_gold, (de_x-1700, de_y-450))
            
            
            
            if game_paused:
                gaming_pause()
                if button_resume.draw(screen):
                    game_paused = False               
                if button_main.draw(screen):
                    game_status = "intro"
                if button_restart.draw(screen):
                    game_status = "game_starting"
                    

                
        # ============================================ 230628 여기화면 조정 예정
        
        if game_status == "game_result":
            gaming_result()
            if button_main2.draw(screen):
                game_status_old = game_status
                game_status = "intro"
            if button_restart2.draw(screen):
                game_status_old = game_status
                game_status = "game_starting"
                
            if button_right.draw(screen):
                game_status = "session_result"
                print("press")
                
        
        if game_status == "session_result":
            # 위에서 session_result 만들어야 함
            session_result()
            
            if button_right.draw(screen):
                game_status = "all_session"
        
        
        if game_status == "all_session":
            # 위에서 session_result 만들어야 함
            all_session()
            



        # ============================================ =======================
        
        
        


            
                
    else:
        screen.blit(for_start, ((de_x-font_x)/2, 500))
    
    
    
    pygame.display.update()
    
    # fps
    clock.tick(60)


pygame.quit()


#%% saving data (complete ver) 
