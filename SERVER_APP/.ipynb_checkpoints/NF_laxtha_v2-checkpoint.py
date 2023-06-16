# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 16:33:27 2022


@author: Jeonghyun Lee / jeonghyun.lee@snu.ac.kr
"""
import numpy as np  # Module that simplifies computations on matrices
import numpy.matlib
from numpy.random import randint
from scipy.fft import fft
from scipy.signal import find_peaks
import time
from datetime import date, datetime
from mne import filter
from copy import copy
import os, sys
from psychopy import visual, core
from psychopy.constants import (NOT_STARTED, STARTED)
import rpyc
from psychopy.hardware import keyboard

class NNFX2_FAA():
    rpy = None;
    subinfo = None;
    baseline_FAA = [[None, None, None]];
    debug = None;
    org_fs = None;
    
    def __init__(self, subinfo, baseline_FAA = [[None, None, None]], debug_mode=False):
        self.subinfo = subinfo;
        self.debug = debug_mode
        self.baseline_FAA = baseline_FAA;
        self.org_fs = 250;
        self.NumNF = 0;


    def set_EEGcalc(self, FFT_win, FFT_slides, SRATE =250):
        """
        Parameters
        ----------
        FFT_win : float
            FFT window size (epoch size; in sec).
        
        FFT_slides : float
            Sliding size. Minimum interval to calculate FFT between epochs. (in sec)
        SRATE : int
            sampling frequency.
        Returns x
        -------
        None.

        """
        self.fs = SRATE;
        self.t_slide = FFT_slides;
        fft_win = FFT_win * self.fs; #% fft window len
        
        #% fft parameter
        k =np.linspace(0,fft_win-1,fft_win); #%fourier time
        T = fft_win/self.fs;  #% frequency interval
        freq = k/T;     #% frequency range
        self.cutOff = int(np.ceil(fft_win/2));  # % Nyquist 어쩌구 
        self.freq = freq[:self.cutOff];
        self.fft_win = fft_win;
        self.freq
        
    def preprocessing(self, eeg, filter_range, noise_thr):
        # low- high- pass filter
        eeg_filtered = filter.filter_data(eeg, self.fs, filter_range[0], filter_range[1],verbose=False);
        
        # noise rejection
        pre_t = round(self.fs*0.2);
        post_t = round(self.fs*0.5);
        
        peak_list = [];
        for chi in range(2):
            data_temp = eeg_filtered[chi,:];
            peaks,_ = find_peaks(np.abs(data_temp),height = 0)
            ov_thre = np.where(np.abs(data_temp) > noise_thr)
            peak_temp = np.intersect1d(peaks, ov_thre);
            peak_list = peak_list + list(peak_temp)
        reject_points = np.unique(peak_list);
        reject_range =[];
        for x in reject_points:
            reject_range = reject_range + list(np.arange(x-pre_t,x+post_t,1))
        reject_range = np.unique(reject_range);
        
        eeg_rejected = copy(eeg_filtered);
        if np.any(reject_range):  # mute if want skip rejection
            down = np.where(reject_range<0)
            reject_range = np.delete(reject_range, down)
            up = np.where(reject_range>=np.shape(eeg_rejected)[1])
            reject_range = np.delete(reject_range, up)
            eeg_rejected[:,reject_range] = 0;
        
        return eeg_rejected 
    
    def calc_asymmetry(self, data_fft, fft_win, cutOff, alpha_idx_range):
        
        alpha_l= alpha_idx_range[0];
        alpha_h= alpha_idx_range[1];
        fft_temp1 = fft(data_fft[0,:]) / fft_win*2; fft1 = np.abs(fft_temp1[0:cutOff]) ;
        fft_temp2 = fft(data_fft[1,:]) / fft_win*2; fft2 = np.abs(fft_temp2[0:cutOff]) ;
        # calculate asymmetry
        F3 = np.mean(fft1[alpha_l:alpha_h+1]);
        # print('F3 : ', str(F3))
        F4 = np.mean(fft2[alpha_l:alpha_h+1]);
        # print('F3 : ', str(F3))
        faa = (F4 - F3)/(F3 + F4);
        return faa
        
    def reject_outliers(self, numarray, m = 3):
        d = np.abs(numarray - np.median(numarray))
        mdev = np.median(d)
        s = d/mdev if mdev else 0
        return np.where(s>m)
    
    def baseline_recording(self, duration=180, noise_thr=75, alpha_range = [8, 13]):
        """
        Parameters
        ----------
        duration : int, optional
            Baseline recording duration (sec). The default is 180.
        noise_thr : int, optional
            Noise threshold for data rejection (in uV). The default is 75.
        alpha_range : [float, float], optional
            Alpha range or other frequency ranges for an assymetry value. The default is [8, 13].

        Returns
        -------
        baseline_FAA :

        """
        try:
            self.rpy = rpyc.connect("localhost", 18861, config = {'allow_all_attrs': True, 'allow_pickle':True})
            pass
        
        except ConnectionRefusedError:
            print('Please run a service code first')
            return
        
        print('Preparing baseline recording')
        print('Press Ctrl-C in the console to break the while loop.')
        self.freq4asymmetry = alpha_range;
        alpha_low = alpha_range[0];
        alpha_high = alpha_range[1];
        alpha_l = np.argmin( np.abs(self.freq- alpha_low));
        alpha_h = np.argmin( np.abs(self.freq- alpha_high));
        temp_buffer = None;
        faa_all = [];
        
        t_init = time.time();
        t_interval = time.time();
        

        # baseline code
        while time.time()-t_init < duration:
            try:
                if time.time()-t_interval < self.t_slide: # wait minimum interval
                    continue
                else: # online-processing
                    temp_buffer = np.array(self.rpy.root.data_storage);
                    time_temp = temp_buffer[4,-int(self.fft_win/2)];
                    # online-processing 1. epoching with the newest data
                    eeg_temp = temp_buffer[:2,-self.fft_win:];
                    
                    # online-processing 2. preprocessing
                    eeg_rejected = self.preprocessing(eeg_temp, [2, 40], noise_thr)
                    
                    # calculate data using fft
                    faa = self.calc_asymmetry(eeg_rejected, self.fft_win, self.cutOff, [alpha_l,alpha_h]);
                    faa_all.append([faa, time.time()-t_init, time_temp])
                    
            except KeyboardInterrupt:
                break
        print('Closing baseline recording...')
    
        # reture baseline FAA
        faa_all_outlierx = np.transpose(np.array(faa_all));
        print(faa_all_outlierx.shape)
        temp = faa_all_outlierx[0,:];
        outidx = self.reject_outliers(temp, 3);
        faa_all_outlierx[0,outidx] = np.NaN
        
        faa_mean = np.nanmean(faa_all_outlierx[0,:]);
        faa_std = np.nanstd(faa_all_outlierx[0,:]);
        duration = faa_all_outlierx[1,-1];
        
        self.baseline_FAA.append([faa_mean, faa_std, duration]);
        faa_all_outlierx = np.transpose(faa_all_outlierx)
        return faa_all_outlierx

    def psypy_setting4NF(self, bg_path, stim_path):
        """
        for 1) Loading stim images 2) setting a PTB window  and 3) get keyboard and window info.
        
        Keyword arguments:
        bg_path : path of a background image.
        stim_path : path of a stim image (kitty face).

        """
        # Psychopy visualizing setting.
        self.vis_status = True           # true --> vis update, false --> noflip
        self.frameTolerance = 0.001      # how close to onset before 'same' frame
        self.endExpNow = False           # flag for 'escape' or other condition => quit the exp
        
        # Initialize components for Routine "trial"
        self.trialClock = core.Clock()
        # Create some handy timers
        self.globalClock = core.Clock()  # to track the time since experiment started
        self.routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

        # keyboard setting
        # create a default keyboard (e.g. to check for escape)
        # self.defaultKeyboard = keyboard.Keyboard(backend='iohub')
        self.defaultKeyboard = keyboard.Keyboard()
        
        # Setup the Window
        self.NF_win = visual.Window(
                size=(1920, 1080), fullscr=False, screen=0,
                winType='pyglet', allowGUI=False, allowStencil=False,
                monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb',
                blendMode='avg', useFBO=True,
                units='height')
        
        # store frame rate of monitor if we can measure it
        framerate= self.NF_win.getActualFrameRate()
        if framerate != None:
            frameDur = 1.0 / round(framerate)
        else:
            frameDur = 1.0 / 60.0  # could not measure, so guess
        self.NF_framerate =framerate;
        self.frameDur = frameDur;
        # Setup ioHub
        self.ioConfig = {}
        # load image
        self.img_background = visual.ImageStim(
            win=self.NF_win,
            name='background', units='height',
            image=bg_path, mask=None, 
            ori=0.0, pos=(0, 0), size=(1.8, 1),
            color=[1, 1, 1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128.0, interpolate=True, depth=-1.0)
        
        self.img_stim = visual.ImageStim(
            win=self.NF_win,
            name='stim',
            image=stim_path,  mask=None,
            ori=0.0, pos=[0, 0], size=(.19,.28),
            color=[1, 1, 1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False,
            texRes=128.0, interpolate=True, depth=-2.0)
        self.key_resp = keyboard.Keyboard();
        self.key_resp.keys = []
        self.key_resp.rt = []
        
    def psypy_visu4NF(self, faa, vs_updater, pre_stim_image_pos, updata_t= .2, std_thrsd=[.85, 5]):
        """
        Neurofeedback visualizing by Psychopy  
        
        Keyword arguments:
        faa                 -- float; faa value for visualizing
        vs_updater          -- list; start value must be [0, 0]
        pre_stim_image_pos  -- float; between -0.5 to 0.5
        update_t            -- float; image update gap (sec)
        std_thrsd           -- list; [std_threshold, max_value];

        """
       
        
        visual_updater_st = vs_updater[0];
        visual_updater_en = vs_updater[1];
        stim_image_pos = pre_stim_image_pos;
        max_height = .40;
        bs_height = -.25;
        
        tThisFlip = self.NF_win.getFutureFlipTime(clock=self.trialClock)
        # update/draw components on each frame
        if self.vis_status == True:
            visual_updater_st = self.trialClock.getTime()
            self.vis_status = False

        visual_updater_en = self.trialClock.getTime()
        update_timing = (visual_updater_en) - (visual_updater_st)
        
        faa_threshold = self.baseline_FAA[-1][0] + self.baseline_FAA[-1][1]*std_thrsd[0];
        # print('faa_threshold : ', str(faa_threshold))
        # print('faa : ', str(faa))
        #position update
        if update_timing > updata_t:
            if faa >= faa_threshold:
                # print('bigger than thres')
                faa_z = (faa - self.baseline_FAA[-1][0]) / self.baseline_FAA[-1][1]
                pos1 = faa_z - std_thrsd[0];
                # print('pos1 : ', str(pos1))
                if pos1 > std_thrsd[1]:
                    # print('max')
                    stim_image_pos = max_height;
                else:
                    # print('under max')
                    stim_image_pos = bs_height + ((max_height - bs_height) * (pos1/std_thrsd[1]))
                        
            else:
                # print('lower than thres')
                faa_z = (faa - self.baseline_FAA[-1][0]) / self.baseline_FAA[-1][1]
                pos1 = faa_z - std_thrsd[0];
                # print('pos1 : ', str(pos1))
                if pos1 < -std_thrsd[1]:
                    stim_image_pos = -max_height;
                else:
                    stim_image_pos = bs_height + ((-max_height - bs_height) * (pos1/std_thrsd[1]))
            print(stim_image_pos)  
            self.vis_status = True
        # else:
            
        # *background* updates
        if self.img_background.status == NOT_STARTED and tThisFlip >= 0.0 - self.frameTolerance:
            self.img_background.setAutoDraw(True)

        # *image_2* updates
        if self.img_stim.status == NOT_STARTED and tThisFlip >= 0.0 - self.frameTolerance:           
            self.img_stim.setAutoDraw(True)
        elif self.img_stim.status == STARTED:  # only update if drawing
            self.img_stim.setPos([0, stim_image_pos], log=False)
        
        self.NF_win.flip()
        
        # *key_resp* updates
        # check for quit (typically the Esc key)
        if self.defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            
        vs_updater[0] = visual_updater_st;
        vs_updater[1] = visual_updater_en;
        
        return vs_updater, stim_image_pos
        
    def Neurofeedback(self, duration=600, noise_thr=75, screen_updata_t = None):
        """
        Neurofeedback.. 
        
        Keyword arguments:
        
        """
        self.NumNF = self.NumNF+1;
        if self.baseline_FAA[-1][0] is None:
            print('Baseline recording must be preceded...')
            return
        if screen_updata_t is None:
            screen_updata_t = self.t_slide
        try:
            self.rpy = rpyc.connect("localhost", 18861, config = {'allow_all_attrs': True, 'allow_pickle':True})
            pass
        
        except ConnectionRefusedError:
            print('Please run a service code first')
            return
        print('Press Ctrl-C in the console to break the while loop.')
        
        faa_all = [];
        
        alpha_low = self.freq4asymmetry[0];
        alpha_high = self.freq4asymmetry[1];
        alpha_l = np.argmin( np.abs(self.freq- alpha_low));
        alpha_h = np.argmin( np.abs(self.freq- alpha_high));
        temp_buffer = None;
        faa_all = [];
        
        t_init = time.time();
        t_interval = time.time();

        
        vs_updater = [0, 0];
        pre_stim_image_pos = -.4;


        _timeToFirstFrame = self.NF_win.getFutureFlipTime(clock="now")
        self.trialClock.reset(-_timeToFirstFrame)  
        while time.time()-t_init < duration:
            try:
                if time.time()-t_interval < screen_updata_t: # wait minimum interval
                    continue
                else: # online-processing
                    temp_buffer = np.array(self.rpy.root.data_storage);
                    time_temp = temp_buffer[4,-int(self.fft_win/2)];
                    
                    # online-processing 1. epoching with the newest data
                    eeg_temp = temp_buffer[:2,-self.fft_win:];
                    
                    # online-processing 2. preprocessing
                    eeg_rejected = self.preprocessing(eeg_temp, [2, 40], noise_thr)
                    
                    # calculate data using fft
                    faa = self.calc_asymmetry(eeg_rejected, self.fft_win, self.cutOff, [alpha_l,alpha_h]);
                    faa_all.append([faa, time.time()-t_init, time_temp])

                
                    # visualize code#####
                    vs_updater, pre_stim_image_pos = self.psypy_visu4NF(faa, vs_updater, pre_stim_image_pos, .2, [.85, 5]);
                
                
            except KeyboardInterrupt:
                print('Closing!')
               
        self.NF_win.close()
        
        faa_all = np.array(faa_all)
        return faa_all
        core.quit()