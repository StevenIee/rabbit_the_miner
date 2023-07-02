# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 19:04:12 2023

@author: Steven 
"""
import numpy as np  # Module that simplifies computations on matrices
import numpy.matlib
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.signal import find_peaks
from mne import filter
from copy import copy

##VARIABLES##
srate = 250; #SAMPLING RATE IN Hz
FFT_win = 5; # seconds / averaging window
FFT_slides = 0.1; # seconds / calculation intervals
filter_range = [2, 40]; # highpass and low pass cutoffs in Hz
noise_thr = 100; # uV voltage threshold for rejection
freq4asymmetry = [8, 13]; # set faa calculation frequency

def set_EEGcalc(FFT_win, SRATE):
    fs = SRATE;
    fft_win_len = FFT_win * fs; #% fft window len
    
    #% fft parameter
    k =np.linspace(0,fft_win_len-1,fft_win_len); #%fourier time
    T = fft_win_len/fs;  #% frequency interval
    freq = k/T;     #% frequency range
    cutOff = int(np.ceil(fft_win_len/2));  # % Nyquist 어쩌구 
    freq = freq[:cutOff];
    return freq, cutOff, fft_win_len

def get_alpha_index(freq, freq4asymmetry):
    alpha_low = freq4asymmetry[0];
    alpha_high = freq4asymmetry[1];
    alpha_l = np.argmin( np.abs(freq- alpha_low));
    alpha_h = np.argmin( np.abs(freq- alpha_high));
    alpha_idx_range = [alpha_l, alpha_h]
    return alpha_idx_range


def preprocessing(eeg, filter_range, noise_thr, srate):
    # low- high- pass filter
    eeg_filtered = filter.filter_data(eeg, srate, filter_range[0], filter_range[1], verbose=False);
    
    # noise rejection
    pre_t = round(srate*0.2);
    post_t = round(srate*0.5);
    
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

def calc_asymmetry( data_fft, fft_win_len, cutOff, alpha_idx_range):
    alpha_l= alpha_idx_range[0];
    alpha_h= alpha_idx_range[1];
    fft_temp1 = fft(data_fft[0,:]) / fft_win_len*2; fft1 = np.abs(fft_temp1[0:cutOff]) ;
    fft_temp2 = fft(data_fft[1,:]) / fft_win_len*2; fft2 = np.abs(fft_temp2[0:cutOff]) ;
    # calculate asymmetry
    F3 = np.mean(fft1[alpha_l:alpha_h+1]);
    # print('F3 : ', str(F3))
    F4 = np.mean(fft2[alpha_l:alpha_h+1]);
    # print('F3 : ', str(F3))
    faa = (F4 - F3)/(F3 + F4);
    return faa

def calc_asymmetry2( data_fft, fft_win_len, cutOff, alpha_idx_range, group_cond):
    alpha_l= alpha_idx_range[0];
    alpha_h= alpha_idx_range[1];
    fft_temp1 = fft(data_fft[0,:]) / fft_win_len*2; fft1 = np.abs(fft_temp1[0:cutOff]) ;
    fft_temp2 = fft(data_fft[1,:]) / fft_win_len*2; fft2 = np.abs(fft_temp2[0:cutOff]) ;
    # calculate asymmetry
    F3 = np.mean(fft1[alpha_l:alpha_h+1]);
    # print('F3 : ', str(F3))
    F4 = np.mean(fft2[alpha_l:alpha_h+1]);
    # print('F3 : ', str(F3))
    if group_cond== 1:
        faa = (F4 - F3)/(F3 + F4);
    else:
        faa = (F3 + F4) / 2;
        
    return faa

def reject_outliers(numarray, m = 3):
    d = np.abs(numarray - np.median(numarray))
    mdev = np.median(d)
    s = d/mdev if mdev else 0
    return np.where(s>m)


def eeg_datasaving(temp_EEG, eegdata, timedata):
    if temp_EEG.shape[0] ==0:
        temp_EEG = np.concatenate((eegdata, timedata));
    else:

        temp_EEG2 = np.concatenate((eegdata, timedata));
        last_t = temp_EEG[2,-1];
        last_t_ind = np.where(timedata == last_t)[0]
        if last_t_ind.shape[0] == 0:
            temp_EEG = np.concatenate((temp_EEG, temp_EEG2), axis=1)
        else:
            last_t_index = last_t_ind[-1];
            temp_EEG2 = temp_EEG2[:,last_t_index:];
            temp_EEG = np.concatenate((temp_EEG, temp_EEG2), axis=1)
    return temp_EEG


def bound_line_plot_save(data, filename):
    x_data = [row[1] for row in data]  # extract second column as x data
    y_data = [row[0] for row in data]  # extract first column as y data
    
    fig, ax = plt.subplots()
    ax.plot(x_data, y_data, marker='o', markersize=8, fillstyle='none', linestyle='--', color='b')
    ax.plot(x_data, y_data, marker='o', markersize=4, color='k')
    l = ax.fill_between(x_data, y_data)
    ax.set_ylabel('Performance')
    ax.set_xlabel('Game time (s)')
    # remove tick marks
    ax.xaxis.set_tick_params(size=0)
    ax.yaxis.set_tick_params(size=0)
    
    # change the color of the top and right spines to opaque gray
    ax.spines['right'].set_color((.8,.8,.8))
    ax.spines['top'].set_color((.8,.8,.8))
    
    # xylim set
    xmax = np.max(x_data);
    xmin = np.min(x_data);
    ax.set_xlim(xmin, xmax)
    
    ymin,ymax =ax.get_ylim();
    ax.set_ylim(0, ymax)
    ax.grid('on')
    
    # xy label
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()
    xlab.set_style('italic')
    xlab.set_size(10)
    ylab.set_style('italic')
    ylab.set_size(10)
    
    
    # change the fill into a blueish color with opacity .3
    l.set_facecolors([[.5,.5,.8,.3]])
    
    # change the edge color (bluish and transparentish) and thickness
    l.set_edgecolors([[0, 0, .5, .3]])
    l.set_linewidths([3])
    
    fig.savefig(filename, dpi=300, bbox_inches='tight')



freq, cutOff , fft_win_len = set_EEGcalc(FFT_win, srate)
alpha_idx_range = get_alpha_index(freq, freq4asymmetry)






    




    