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
    root = tk.TK()
    root.geometry('500x450')
    root.eval('tk::PlaceWindow . center')
    root.title("참여자 정보")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
def on_closing():
    sys.exit()
    
    
class PlayerInfoForm(tk.Tk):
    def __init__(self, default_values, tests):
        super().__init__()

        self.player_id = tk.StringVar()
        self.session_num = tk.StringVar()
        self.stage_num = tk.StringVar()
        self.manual_faa_mean = tk.StringVar()
        self.manual_faa_std = tk.StringVar()

        self.player_id.set(default_values[0])
        self.session_num.set(default_values[1])
        self.stage_num.set(default_values[2])
        self.manual_faa_mean.set(default_values[3])
        self.manual_faa_std.set(default_values[4])

        self.tests = tests

        create_gui()
        self.create_widgets()

    def create_widgets(self):
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

class PlayerInfoForm(tk.Tk):
    def __init__(self, default_values, tests):
        super().__init__()

        self.player_id = tk.StringVar()
        self.session_num = tk.StringVar()
        self.stage_num = tk.StringVar()
        self.manual_faa_mean = tk.StringVar()
        self.manual_faa_std = tk.StringVar()

        self.player_id.set(default_values[0])
        self.session_num.set(default_values[1])
        self.stage_num.set(default_values[2])
        self.manual_faa_mean.set(default_values[3])
        self.manual_faa_std.set(default_values[4])

        self.tests = tests

        create_gui()
        self.create_widgets()

    def create_widgets(self):
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
        
    def validate_inputs(player_id, session_num, stage_num, manual_faa_mean, manual_faa_std):
        if not is_number(player_id):
            return False
        if not is_number(session_num):
            return False
        if not is_number(stage_num):
            return False
        if not is_number(manual_faa_mean):
            return False
        if not is_number(manual_faa_std):
            return False
    
        stage_num = int(stage_num)
        
        if stage_num < 1 or stage_num > 5:
            return False
        elif stage_num != 1 and (float(manual_faa_mean) == 0 or float(manual_faa_std) == 0):
            return False
    
        return True

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
        if self.validate_inputs():
            self.print_player_info()
            self.destroy()
        else:
            messagebox.showerror("Invalid Input", "Please enter valid player information.")

    '''
def player_input():
    player_id = player_id_entry.get()
    session_num = session_num_entry.get()
    stage_num = stage_num_entry.get()
    manual_faa_mean = manual_faa_mean_entry.get()
    manual_faa_std = manual_faa_std_entry.get()

    if validate_inputs(player_id, session_num, stage_num, manual_faa_mean, manual_faa_std):
        print_player_info(player_id, session_num, stage_num, manual_faa_mean, manual_faa_std)
        root.destroy()
    else:
        messagebox.showerror("Invalid Input", "Please enter valid player information.")

    submit_button = tk.Button(root, text="Submit", command=submit_player_info)
    submit_button.pack()

    root.mainloop()
        '''
    
    
def player_data(player_info_is_good, tests):
    global root, data_path
    
    create_gui()
    
    data_path = org_path + '/data'
    
    if not os.path.isdier(data_path):
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

    player_id_default_text = "type integer" if not tests[0] else "999"
    session_default_text = "type integer" if not tests[1] else "999"
    stage_num_default_text = "type integers 1 to 5" if not tests[2] or not tests[5] else "1"
    manual_mfm_default_text = "enter faa mean in float" if not tests[3] else "0"
    manual_mfs_default_text = "enter faa std in float" if not tests[4] else "0"
    if not tests[6]:
        stage_num_default_text = "faa is 0 for stage 1"
        manual_mfs_default_text = "0"
        manual_mfm_default_text = "0"