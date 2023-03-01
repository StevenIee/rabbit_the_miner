# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 19:04:12 2023

@author: Steven 
"""
import numpy as np  # Module that simplifies computations on matrices
import numpy.matlib
from scipy.fft import fft
from scipy.signal import find_peaks
import mne
import copy


srate = 250;
FFT_win = 5;
FFT_slides = 0.1;
filter_range = [2, 40];
noise_thr = 100;
freq4asymmetry = [8, 13];


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


def preprocessing( eeg, filter_range, noise_thr, srate):
    # low- high- pass filter
    eeg_filtered = mne.filter.filter_data(eeg, srate, filter_range[0], filter_range[1]);     
    
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
    
    eeg_rejected = copy.copy(eeg_filtered);
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


def reject_outliers(numarray, m = 3):
    d = np.abs(numarray - np.median(numarray))
    mdev = np.median(d)
    s = d/mdev if mdev else 0
    return np.where(s>m)

freq, cutOff , fft_win_len = set_EEGcalc(FFT_win, srate)
alpha_idx_range = get_alpha_index(freq, freq4asymmetry)






    




    