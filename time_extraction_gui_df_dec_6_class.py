#!/usr/bin/env python
# coding: utf-8

# In[6]:


# genral imports, you may not need all of these. But i dont know which ones you do you need soo....
import numpy as np
import os,sys,glob
import pandas as pd
import time
from datetime import timedelta
from timeit import default_timer as timer
import math
import serial
from os import system
#general imports
import h5py
from itertools import product
import matplotlib.pyplot as plt


# In[7]:



def extract_waveform_timestamps(gui_csv_path, recording_path):
    
    ##### read in and memory map the analog channels to their own variable
    
    def sglx_nidaq_analog(bin_path, seconds=True):
    
        #Memory map the bin file and parse into binary lines
        mm = np.memmap(glob.glob(os.path.join(bin_path))[0],dtype='int16')
        a0 = mm[0::9]
        a1 = mm[1::9]
        a2 = mm[2::9]
        a3 = mm[3::9]
        a4 = mm[4::9]
        a5 = mm[5::9]
        a6 = mm[6::9]
        a7 = mm[7::9]
        analog = {'a0': a0, 'a1': a1, 'a2': a2, 'a3': a3, 'a4': a4, 'a5': a5, 'a6': a6, 'a7': a7}
        return analog
    
    analog = sglx_nidaq_analog(recording_path)
    a0 = analog.get('a0')
    a1 = analog.get('a1')
    a2 = analog.get('a2')
    a3 = analog.get('a3')
    a4 = analog.get('a4')
    a5 = analog.get('a5')
    a6 = analog.get('a6')
    a7 = analog.get('a7')
    
    a3_down = a3[::10] #trigger
    a4_down = a4[::10] #Electrical
    a5_down = a5[::10] #Optical
    a6_down = a6[::10] #Run
    
    gui_data_frame = pd.read_csv(gui_csv_path)
    
    #### place all waveforms per channel into their own array (wrs,ers,ors)
    
    #### rrs (run_button)
    run_timestamps_high = np.where(a6_down>10000)[0]
    rrs = []
    for transition in np.where(np.diff(run_timestamps_high)>10)[0]:
        rrs.extend([run_timestamps_high[transition]])
    rrs.extend([run_timestamps_high[-1]])
    rrs = np.array(rrs)
    
    ### ers (trigger)
    
    e_high_samples = np.where(a3_down<15000)[0]
    e_low_samples = np.where(a3_down>15000)[0]
    ers_list = []
    efs_list = [e_low_samples[-1]]
    for transition in np.where(np.diff(e_high_samples)>50)[0]:
        ers_list.extend([e_high_samples[transition]])
    for transition in np.where(np.diff(e_low_samples)>50)[0]:
        efs_list.extend([e_low_samples[transition]])
    
    ers_list.append(e_high_samples[-1])
    ers = np.array(ers_list)
    efs = np.array(efs_list)
   
    #### wrs (electrical)
    w_high_samples = np.where(a4_down>100)[0]
    w_low_samples = np.where(a4_down<-100)[0]
    
    wrs_list = []
    wfs_list = []
    for transition in np.where(np.diff(w_high_samples)>10)[0]:
        wrs_list.extend([w_high_samples[transition]]) 
    for transition in np.where(np.diff(w_low_samples)>10)[0]:
        wfs_list.extend([w_low_samples[transition]+9])

    wrs_list.append(w_high_samples[-1])
    wrs = np.array(wrs_list)
    wfs = np.array(wfs_list)
    
    #### create parameter duration column, append it to gui_data_frame
    
    gui_data_frame['parameter_duration'] = gui_data_frame.apply(lambda row: ((0.005 + 0.0005 + row.E_duration + row.E_O_offset + row.O_duration + row.Time_between_pulses) * row.pulse_number)*row.number_of_trains + (row.time_between_trains  * (row.number_of_trains-1)) , axis = 1)

    parameter_row_0 = gui_data_frame[gui_data_frame['Unnamed: 0'] == 0]
    # gui_data_frame = parameter_row_0
  
    parameter_durations = parameter_row_0.parameter_duration
    parameter_durations_list = parameter_durations.tolist()
    
    #### trigger timestamp extraction, for each parameter
    
    first_trigger_per_parameter = []

    for a1 in rrs:
        for a2 in ers:
            if (a2/1e5 - a1/1e5)<0.031 and (a2/1e5 - a1/1e5)>0:
                first_trigger_per_parameter.append(a2) 


    parameter_trigger_start = np.array(first_trigger_per_parameter)
    ers_start = parameter_trigger_start
    
    trigger_duration_samples = []
    for a1 in parameter_durations_list:
        trigger_duration_samples.append(int(a1 * 1e5))

    end_of_parameter_trigger = trigger_duration_samples + ers_start
    
    ers_end = [end_of_parameter_trigger[x] for x in range(len(rrs))]

    ers_end = np.array(ers_end)
    ers_end_min = []
    for num in range(len(rrs)):
        ers_end_min.append(min(ers, key=lambda x:abs(x - ers_end[num])))


    ers_end = ers_end_min
    
    parameters_ers = []

    for num in range(len(ers_start)):
        parameters_ers.extend([[(ers_start[num]),(ers_end[num])]])

    ers_paramters_in_seconds = np.array(parameters_ers)

    ers_parameters_index = []

    for num in range(len(ers_start)):
        ers_parameters_index.extend([[ers_list.index(ers_start[num]),ers_list.index(ers_end[num])]])
        
    t_parameters_start = []
    t_parameters_end = []

    for num in range(len(rrs)):
        t_parameters_start.extend([ers_list.index(ers_start[num])])
        t_parameters_end.extend([ers_list.index(ers_end[num])])
        
    t_parameter_full = []
    for num in range(len(rrs)):
        t_parameter_full.extend([ers[t_parameters_start[num]:t_parameters_end[num]+1]])

    all_trigger_waveforms_list = []
    for num in range(len(t_parameter_full)):
        parameter_time_stamps = t_parameter_full[num]/1e5
        all_t_data = {
            'trigger_time_stamps (sec)': [parameter_time_stamps],

        }

        all_t_data_df = pd.DataFrame(all_t_data)
        all_trigger_waveforms_list.append(all_t_data_df)

    concat_trigger_df = pd.concat(all_trigger_waveforms_list,ignore_index=True)
   
    #### Electrical Timestamp extraction for each parameter
    
    
    first_e_per_parameter = []

    for a1 in rrs:
        for a2 in wrs:
            if (a2/1e5 - a1/1e5)<0.035 and (a2/1e5 - a1/1e5)>0:
                first_e_per_parameter.append(a2) 

    parameter_electrical_start = np.array(first_e_per_parameter)
    wrs_start = parameter_electrical_start

    
    parameter_duration_0 = []

    duration_samples = []
    for a1 in parameter_durations_list:
        duration_samples.append(int(a1 * 1e5))

    end_of_parameter_e = duration_samples + wrs_start
    
    wrs_end = [end_of_parameter_e[x] for x in range(len(rrs))]
    wrs_end = np.array(wrs_end)
    
    wrs_end_min = []
    for num in range(len(rrs)):
        wrs_end_min.append(min(wrs, key=lambda x:abs(x - wrs_end[num])))

    wrs_end = wrs_end_min
    
    parameters_wrs = []

    for num in range(len(wrs_start)):
        parameters_wrs.extend([[(wrs_start[num]),(wrs_end[num])]])

    wrs_paramters_in_seconds = np.array(parameters_wrs)
    
    wrs_end_min = []
    for num in range(len(rrs)):
        wrs_end_min.append(min(wrs, key=lambda x:abs(x - wrs_end[num])))
        
    wrs_parameters_index = []

    for num in range(len(wrs_start)):
        wrs_parameters_index.extend([[wrs_list.index(wrs_start[num]),wrs_list.index(wrs_end[num])]])
        
    e_parameters_start = []
    e_parameters_end = []

    for num in range(len(rrs)):
        e_parameters_start.extend([wrs_list.index(wrs_start[num])])
        e_parameters_end.extend([wrs_list.index(wrs_end[num])])
        
    e_parameter_full = []
    for num in range(len(rrs)):
        e_parameter_full.extend([wrs[e_parameters_start[num]:e_parameters_end[num]+1]])
        
    all_electrical_waveforms_list = []
    for num in range(len(e_parameter_full)):
        
        parameter_time_stamps = e_parameter_full[num]/1e5
        all_e_data = {
            'electrical_time_stamps_seconds': [parameter_time_stamps],
        }
        all_e_data_df = pd.DataFrame(all_e_data)
        all_electrical_waveforms_list.append(all_e_data_df)


    concat_electrical_df = pd.concat(all_electrical_waveforms_list,ignore_index=True)
    
    
    return concat_electrical_df.head(30), concat_trigger_df.head(30)


  


# In[8]:



recording_path = r'/Volumes/ROCKET-nano/denman_lab/dbs_files/dbs_recording_data_raw/real/20211129_jlh2_estim_g1_t0.nidq.bin' #mac
gui_csv_path = '/Users/granthughes/Desktop/Denman_lab/dbs_files/data_frames/dbs_run_dataframes/Concat_runs_df/2021-12-06_16-28-32.csv'


extract_waveform_timestamps(gui_csv_path, recording_path)


# In[ ]:




