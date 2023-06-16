# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 15:18:30 2022

@author: Jeonghyun Lee / jeonghyun.lee@snu.ac.kr
"""
from datetime import date
from NF_laxtha_v2 import NNFX2_FAA
# =============================================================================
# # import subprocess
# # #%% 1. Start the main visualizer
# # # choose a proper comport and click [기기연결]
# # proc = subprocess.Popen(["python" ,"main.py"], stdout=subprocess.PIPE, shell = True)
# # #%% 2. Open a server for data buffer
# # proc2 = subprocess.Popen(["python" ,"app_test1.py"], stdout=subprocess.PIPE, shell = True)
# =============================================================================
#% 1. Start the main visulaizer and server
# prompt1) -> choose a proper comport and click [기기연결]
# >>> conda activate nnfx2
# >>> cd C:\Users\leelab_laptop1\Desktop\WCD_EEG\nnfx2_ver3
# >>> python main.py


# prompt2) opne server
# >>> conda activate nnfx2
# >>> cd C:\Users\leelab_laptop1\Desktop\WCD_EEG\nnfx2_ver3
# >>> python app_test1.py

#%% 2. Get subject info and date
sn = input('subjectname?:');
datemd = date.today().strftime("%m_%d_");
subject_info = datemd + sn;

#%% 3. Baseline
NF1 = NNFX2_FAA(subject_info);

NF1.set_EEGcalc(5, 0.1);
faa_all = NF1.baseline_recording(180, 1000, [8, 13]) # <- duration set

print('Baseline FAA results')
print(['FAA (mean) : ', str(NF1.baseline_FAA[-1][0])])
print(['FAA (std) : ', str(NF1.baseline_FAA[-1][1])])
print(['Duration : ', str(NF1.baseline_FAA[-1][2])])


baselinefn = subject_info + '_baseline.csv';
with open(baselinefn, 'w') as file:
    header1 = 'FAA (mean) : '+ str(NF1.baseline_FAA[-1][0]);
    header2 = 'FAA (std) : '+ str(NF1.baseline_FAA[-1][1]);
    header3 = 'Duration : '+ str(NF1.baseline_FAA[-1][2]);
    file.write(header1 + '\n')
    file.write(header2 + '\n')
    file.write(header3 + '\n')
    file.write('FAA,time_relative,time_absolute\n')
    for row in faa_all:
        s = ",".join(map(str, row))
        file.write(s+'\n')
file.close();


#%%
#%% 4. Neurofeedback session
#%% 
# set psycopy 
bg_path = '.\\background1.png'
stim_path = '.\\set2_happy_yel_4_yel.png'
NF1.psypy_setting4NF(bg_path, stim_path)

#% play neurofeedback
alpha_range = [8, 13];
faa_all = NF1.Neurofeedback(600, 1000, 0.1)
#%% save neurofeedback
NFfn = subject_info + '_NF' + str(NF1.NumNF)+ '.csv';
with open(NFfn, 'w') as filenf:
    filenf.write('FAA,time_relative,time_absolute\n')
    for row in faa_all:
        s = ",".join(map(str, row))
        filenf.write(s+'\n')
filenf.close();