#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pylab import *
from tkinter import *
import math
import serial
import tkinter as tk
import pyfirmata
import time
import threading 
import pandas as pd
import timeit
from timeit import default_timer as timer
from pyfirmata import Arduino 
from os import system
from timeit import default_timer as timer
from datetime import timedelta
root = Tk()
root.title("DBS Trigger Control")
root.geometry("870x350")
e = Entry(root)
n = 0

recording_number = []
parameter = []
notes = []
number_of_trains = 1;run_x_times_ = number_of_trains

o_1_start = 0
o_1_end = 0
o_2_start = 0
o_2_end = 0
o_3_start = 0
o_3_end = 0
o_4_start = 0
o_4_end = 0
o_5_start = 0
o_5_end = 0
o_6_start = 0
o_6_end = 0
o_7_start = 0
o_7_end = 0
o_8_start = 0
o_8_end = 0




#o_duration = 0
#o_delay = 0




pulse_number = 0
number_of_trains = 1;run_x_times = number_of_trains
time_between_pulses = 0
time_between_trains = 0
pulse_number = 0


# In[ ]:


entry = tk.Entry(root)
variable=StringVar()


# In[ ]:


path = '/Users/granthughes/Desktop/eo_stim/data_frames/1_gui_runs_csv/12_09_21_test/'


# In[ ]:


#Arduino port designation
board = Arduino('/dev/cu.usbmodem14101')


# In[ ]:



t0 = time.time()

def do_train():
#     current_elapsed = timeit.timeit()
   
  
    
    # Update vars
    recording_number.append(recording_number_window.get())
    parameter.append(parameter_window.get())
    notes.append(notes_window.get())
    
    o_1_start = float(o_1_start_entry.get())
    o_1_end = float(o_1_end_entry.get())

    o_2_start = float(o_2_start_entry.get())
    o_2_end = float(o_2_end_entry.get())

    o_3_start = float(o_3_start_entry.get())
    o_3_end = float(o_3_end_entry.get())

    o_4_start = float(o_4_start_entry.get())
    o_4_end = float(o_4_end_entry.get())

    o_5_start = float(o_5_start_entry.get())
    o_5_end = float(o_5_end_entry.get())

    o_6_start = float(o_6_start_entry.get())
    o_6_end = float(o_6_end_entry.get())

    o_7_start = float(o_7_start_entry.get())
    o_7_end = float(o_7_end_entry.get())

    o_8_start = float(o_8_start_entry.get())
    o_8_end = float(o_8_end_entry.get())
    
    
    train_number = float(run_x_times_entry.get())
    pulse_number = float(pulse_num_entry.get())
    time_between_pulses = float(time_between_pulses_entry.get())
    time_between_trains = float(time_between_trains_entry.get())
   
  
    

    all_data_df = {
        'run': [recording_number[-1]]*int(train_number),
        'parameter': [parameter[-1]]*int(train_number),
        'notes': [notes[-1]]*int(train_number),
        

#         'o_duration': [o_duration] *int(train_number),
#         'o_delay': [o_delay]* int(train_number),
        
        'o_1_start': [o_1_start]*int(train_number),
        'o_1_end': [o_1_end]*int(train_number),
        
        'number_of_trains': [train_number]*int(train_number),
        'pulse_number': [pulse_number]*int(train_number),
        'time_between_pulses': [time_between_pulses]* int(train_number),
        'time_between_trains': [time_between_trains]*int(train_number),
    }
        
   
    start_stop_l = [[o_1_start,o_1_end],[o_2_start,o_2_end],[o_3_start,o_3_end],[o_4_start,o_4_end],[o_5_start,o_5_end],[o_6_start,o_6_end],[o_7_start,o_7_end],[o_8_start,o_8_end]]
    
    channel_states = [False,False,False,False,False,False,False,False]
    board_pins= [13,12,11,10,9,8,7,6]
    
    idx, max_time= max(start_stop_l, key=lambda item: item[1])
#     stop_times = []
#     stop_times.append(start_stop_l[i][1])
#     max_stop_time = max(stop_times)
                                               
    current_elapsed_s = time.process_time()
    current_elapsed = 0
    
    # Want the 100 to be the highest value in the start_stop_l + 1
   

    for train in range(int(train_number)):
        print('here')
        for pulse in range(int(pulse_number)):
            current_elapsed_s = time.process_time()
            
            print("train "+str(train+1)+"  pulse "+str(pulse+1))
            current_elapsed = 0
            print(current_elapsed)
            while current_elapsed < (max_time+2):
                current_elapsed = time.process_time() - current_elapsed_s
        
                for i in range(len(start_stop_l)):

                    if current_elapsed > start_stop_l[i][0] and current_elapsed < start_stop_l[i][1] and channel_states[i]==False:

                        print('starting_pin_'+str(i))
                        print(current_elapsed)
                        board.digital[board_pins[i]].write(1)
                        channel_states[i]=True

                    elif current_elapsed > start_stop_l[i][0] and current_elapsed > start_stop_l[i][1] and channel_states[i]==True:

                        print('stopping_pin_'+str(i))
                        print(current_elapsed)
                        board.digital[board_pins[i]].write(0)
                        channel_states[i]=False

#             train_counter = train+1
#             Current_Loop_Number.config(text="Train Number Completed: " + str(train_counter))
#             update_counter()
            
            time.sleep(time_between_pulses)
            

        time.sleep(time_between_trains)

    return all_data_df


# In[ ]:


# # GUI window Control

#Tkinter Windows

app = Frame(root)
app.grid()

startx = Button(app, text='Run Train', command=do_train,fg='green')

## text_windows
recording_number_label = Label(app, text='run_number')
recording_number_window = Entry(app, text='')

parameter_label = Label(app, text='parameter')
parameter_window = Entry(app, text='')

notes_label = Label(app, text='Notes')
notes_window = Entry(app, text='')

### Int_windows
# o_duration_label = Label(app, text= "Optical Pulse Duration (sec)")
# o_duration_entry = Entry(app, text="Optical Duration Seconds")
# o_duration_entry.insert(0,o_duration)

# o_delay_label = Label(app, text= "o_delay")
# o_delay_entry = Entry(app, text="o_delay")
# o_delay_entry.insert(0,o_delay)

start_label = Label(app, text = 'start (t0)')
end_label = Label(app, text = 'end (te)')

o_1_start_entry = Entry(app, text = '')
o_1_start_entry.insert(0,o_1_start)
o_1_end_entry = Entry(app, text='')
o_1_end_entry.insert(0,o_1_end)


o_2_start_entry = Entry(app, text = '')
o_2_start_entry.insert(0,o_2_start)
o_2_end_entry = Entry(app, text='')
o_2_end_entry.insert(0,o_2_end)

o_3_start_entry = Entry(app, text = '')
o_3_start_entry.insert(0,o_3_start)
o_3_end_entry = Entry(app, text='')
o_3_end_entry.insert(0,o_3_end)

o_4_start_entry = Entry(app, text = '')
o_4_start_entry.insert(0,o_4_start)
o_4_end_entry = Entry(app, text='')
o_4_end_entry.insert(0,o_4_end)

o_5_start_entry = Entry(app, text = '')
o_5_start_entry.insert(0,o_5_start)
o_5_end_entry = Entry(app, text='')
o_5_end_entry.insert(0,o_5_end)

o_6_start_entry = Entry(app, text = '')
o_6_start_entry.insert(0,o_6_start)
o_6_end_entry = Entry(app, text='')
o_6_end_entry.insert(0,o_6_end)

o_7_start_entry = Entry(app, text = '')
o_7_start_entry.insert(0,o_7_start)
o_7_end_entry = Entry(app, text='')
o_7_end_entry.insert(0,o_7_end)

o_8_start_entry = Entry(app, text = '')
o_8_start_entry.insert(0,o_8_start)
o_8_end_entry = Entry(app, text='')
o_8_end_entry.insert(0,o_8_end)




pulse_num_label = Label(app, text="(pulse_number) Number_of_pulses_per_train", fg='#9900ff')
pulse_num_entry = Entry(app, text="")
pulse_num_entry.insert(0,pulse_number)

time_between_trains_label = Label(app, text="Time_between_trains (sec)",fg='#9900ff')
time_between_trains_entry = Entry(app, text="")
time_between_trains_entry.insert(0,time_between_trains)

run_x_times_label = Label(app, text="Number_of_trains",fg='#9900ff')
run_x_times_entry = Entry(app, text= "")
run_x_times_entry.insert(0,run_x_times)

time_between_pulses_label = Label(app, text="Time_between_pulses (sec)")
time_between_pulses_entry = Entry(app, text="")
time_between_pulses_entry.insert(0,time_between_pulses)


Current_Loop_Number = Label(app, text = "Train Number Completed: " + str(n),fg='#9900ff')


e1 = tk.Entry(root)

# Gui Layout

startx.grid(row=1, column=0)

## text_windows
recording_number_label.grid(row=2, column=0)
recording_number_window.grid(row=3, column=0)

parameter_label.grid(row=4, column=0)
parameter_window.grid(row=5, column=0)

notes_label.grid(row=6, column=0)
notes_window.grid(row=7, column=0)

## int_windows

# o_duration_label.grid(row=1, column=1)
# o_duration_entry.grid(row=2, column=1)

# o_delay_label.grid(row=3, column=1)
# o_delay_entry.grid(row=4, column=1)


start_label.grid(row=1, column=1)
end_label.grid(row=1, column =2)

o_1_start_entry.grid(row=2, column=1)
o_1_end_entry.grid(row=2, column =2)

o_2_start_entry.grid(row=3, column=1)
o_2_end_entry.grid(row=3, column =2)

o_3_start_entry.grid(row=4, column=1)
o_3_end_entry.grid(row=4, column =2)

o_4_start_entry.grid(row=5, column=1)
o_4_end_entry.grid(row=5, column =2)

o_5_start_entry.grid(row=6, column=1)
o_5_end_entry.grid(row=6, column =2)

o_6_start_entry.grid(row=7, column=1)
o_6_end_entry.grid(row=7, column =2)

o_7_start_entry.grid(row=8, column=1)
o_7_end_entry.grid(row=8, column =2)

o_8_start_entry.grid(row=9, column=1)
o_8_end_entry.grid(row=9, column =2)






run_x_times_label.grid(row=1, column=3)
run_x_times_entry.grid(row=2, column=3)

pulse_num_label.grid(row=3, column=3) 
pulse_num_entry.grid(row=4, column=3) 

time_between_pulses_label.grid(row=5, column=3)
time_between_pulses_entry.grid(row=6, column=3)

time_between_trains_label.grid(row=7, column=3) 
time_between_trains_entry.grid(row=8, column=3) 



root.mainloop()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




