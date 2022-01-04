#!/usr/bin/env python
# coding: utf-8

# In[2]:


from pylab import *
from tkinter import *
import math
import serial
import tkinter as tk
import pyfirmata
import time
import threading 
import pandas as pd
from pyfirmata import Arduino 
from os import system
from timeit import default_timer as timer
from datetime import timedelta
root = Tk()
root.title("DBS Trigger Control")
root.geometry("675x525")
e = Entry(root)
n = 0
L = 0
N = 0
x = 0
running = "" 
run = ""

E_O_offset = 0.001 #Updates time.sleep() 
O_Duration = 0.01 #Updates time.sleep()
E_duration = 0.001

Time_between_pulses = 0
pulse_number = 0

time_between_trains = 0
number_of_trains = 1;run_x_times_ = number_of_trains
#train_counter = count
recording_notess = []
recording_notesss = []
recording_number = []

pulse_train = []
amplitude = []
polarity = []
pulse_width = []
frequency = []
wave_shape = []
cycles = []

entry = tk.Entry(root)
variable=StringVar()


# In[ ]:


#Arduino port designation
board = Arduino('/dev/cu.usbmodem14101')


# In[ ]:


def startx():
    """Enable scanning by setting the global flag to True."""
    global run 
    run = True
    print("Running code " + str(run_x_times_entry.get()) + " times")


# In[1]:


[3]*5


# In[1]:

count = 0 
def do_train():
    # records the timestamp when the run button is clicked  
    board.digital[9].write(1) # red cord / Run button / 
    board.digital[9].write(0)
    print("run button timestamp recorded")
    
    # Update vars
    E_O = float(E_O_Entry.get())  #Updates time.sleep() 
    O_Duration = float(O_Duration_Entry.get())
    E_duration = 0.001 #hardcoded
    Time_between_pulses = float(Time_between_pulses_entry.get())
    pulse_number = float(pulse_num_entry.get())
    time_between_trains = float(time_between_trains_entry.get())
    train_number = float(run_x_times_entry.get())
    recording_notess.append(text_window.get())
    recording_notesss.append(text_1_window.get())
    recording_number.append(text_2_window.get())
    
    pulse_train.append(pulse_train_text_window.get())
    wave_shape.append(wave_shape_text_window.get())
    amplitude.append(amplitude_text_window.get())
    polarity.append(polarity_text_window.get())
    pulse_width.append(polarity_text_window.get())
    frequency.append(frequency_text_window.get())
    wave_shape.append(wave_shape_text_window.get())
    cycles.append(cycles_text_window.get())
    

    all_data = {
        'parameter_number': [recording_number[-1]]*int(train_number),
        'parameter': [recording_notess[-1]]*int(train_number),
        'pulse_train': [pulse_train[-1]]*int(train_number),
        'wave_shape': [wave_shape[-1]]*int(train_number),
        'amplitude': [amplitude[-1]]*int(train_number),
        'polarity': [polarity[-1]]*int(train_number),
        'pulse_width': [pulse_width[-1]]*int(train_number),
        'frequency': [frequency[-1]]*int(train_number),
        'wave_shape': [wave_shape[-1]]*int(train_number),
        'notes': [recording_notesss[-1]]*int(train_number),
        'cycles': [cycles[-1]]*int(train_number),
        
        'E_duration': [E_duration] *int(train_number),
        'E_O_offset' : [E_O_offset]*int(train_number), 
        'O_duration': [O_Duration] *int(train_number),
        'Time_between_pulses': [Time_between_pulses]*int(train_number),
        'pulse_number': [pulse_number]*int(train_number),
        'time_between_trains': [time_between_trains]*int(train_number),
        'number_of_trains': [train_number]*int(train_number),
  
        
        
    }
#     all_data = [[float(E_O_Entry.get()),float(O_Duration_Entry.get()),float(pulse_delay_entry.get()),float(pulse_num_entry.get()),float(train_delay_entry.get()),recording_notess[-1],recording_notesss[-1]]]
    all_data_df = pd.DataFrame(all_data)

    
    
    timestamp_string = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    path = '/Users/granthughes/Desktop/Denman_lab/dbs_files/data_frames/dbs_run_dataframes/'
    recording_folder = 'jhl2_test/'
    
    all_data_df.to_csv(path +recording_folder + timestamp_string + '.csv')
        

    print(all_data_df)
    
    
    for train in range(int(number_of_trains)):
        for pulse in range(int(pulse_number)):
            print("train "+str(train+1)+"  pulse "+str(pulse+1))
             #******start single pulse sequence

            count += 1
            
            board.digital[13].write(1) #Orange cord /m Electrode / Blue Line 
            time.sleep(E_duration)
            board.digital[13].write(0)
            
            time.sleep(E_O_offset) #Add input in gooey for this time

            board.digital[7].write(1) # Yellow cord / Light / Yellow Line
            time.sleep(O_Duration) #Add input in gooey for duration
            board.digital[7].write(0)
            
            train_counter = train+1
            Current_Loop_Number.config(text="Train Number Completed: " + str(train_counter))
            update_counter()
            time.sleep(Time_between_pulses)
            #********end single pulse sequence
        time.sleep(time_between_trains)
        print(count)
    
    return all_data_df, count
        


# In[6]:



def update_counter():
    Current_Loop_Number.config(text="Train Number Completed: " + str(train_counter+1))


# In[13]:





# In[7]:


# # GUI window Control

#Tkinter Window / Button Design code
app = Frame(root)
app.grid()
clicked = StringVar()
clicked_pulse = StringVar()
clicked_polarity = StringVar()
# start = Button(app, text="Run Indefinitely", fg = "green", command=start)
# startx = Button(app, text='Run Train', command=startx,fg='#9900ff')
startx = Button(app, text='Run Train', command=do_train,fg='green')
# stop = Button(app, text="Stop", fg = "red", command=stop)
# reset = Button(app, text="Close Program", fg="orange", command=reset)
text_Label = Label(app, text='parameter')
text_window = Entry(app, text='')

text_1_Label = Label(app, text='Notes')
text_1_window = Entry(app, text='')

text_2_Label = Label(app, text='parameter_number')
text_2_window = Entry(app, text='')

cycles_text_Label = Label(app, text='cycles')
cycles_text_window = Entry(app, text='')

pulse_train_text_Label = Label(app, text='pulse or train')
pulse_train_text_window = OptionMenu(app, clicked_pulse, 'pulse','train',command=callback)

amplitude_text_Label = Label(app, text='amplitude (V)')
amplitude_text_window = Entry(app, text='')

polarity_text_Label = Label(app, text='polarity')
polarity_text_window = OptionMenu(app, clicked_polarity, 'Anode', 'Cathode', 'Biphasic')

pulse_width_text_Label = Label(app, text='pulse_width (μs)')
pulse_width_text_window = Entry(app, text='')

frequency_text_Label = Label(app, text='frequency (Hz)')
frequency_text_window = Entry(app, text='')

wave_shape_text_Label = Label(app, text='wave_shape')
wave_shape_text_window = OptionMenu(app, clicked, 'Biphasic','Tri_Phasic','other')



E_O_Label = Label(app, text= "Time b/t Elec. and Optical onset (sec)")
E_O_Entry = Entry(app, text ="E_O Duration Seconds",)

E_O_Entry.insert(0,E_O_offset)

O_Duration_Label = Label(app, text= "Optical Pulse Duration (sec)")
O_Duration_Entry = Entry(app, text="Optical Duration Seconds")

O_Duration_Entry.insert(0,O_Duration)

run_x_times_label = Label(app, text="Number_of_trains",fg='#9900ff')
run_x_times_entry = Entry(app, text= "")
run_x_times_entry.insert(0,run_x_times_)

time_between_trains_label = Label(app, text="Time_between_trains (sec)",fg='#9900ff')
time_between_trains_entry = Entry(app, text="")
time_between_trains_entry.insert(0,time_between_trains)

Time_between_pulses_label = Label(app, text="Time_between_pulses (sec)")
Time_between_pulses_entry = Entry(app, text="")
Time_between_pulses_entry.insert(0,Time_between_pulses)


pulse_num_label = Label(app, text="(pulse_number) Number_of_pulses_per_train", fg='#9900ff')
pulse_num_entry = Entry(app, text="")
pulse_num_entry.insert(0,pulse_number)

Current_Loop_Number = Label(app, text = "Train Number Completed: " + str(n),fg='#9900ff')




e1 = tk.Entry(root)
## column 0


text_2_Label.grid(row=4, column=0)
text_2_window.grid(row=5, column=0)

pulse_train_text_Label.grid(row=6, column=0)
pulse_train_text_window.grid(row=7, column=0)

polarity_text_Label.grid(row=8, column=0)
polarity_text_window.grid(row=9, column=0)

wave_shape_text_Label.grid(row=10, column=0)
wave_shape_text_window.grid(row=11, column=0)

amplitude_text_Label.grid(row=12, column=0)
amplitude_text_window.grid(row=13, column=0)

pulse_width_text_Label.grid(row=14, column=0)
pulse_width_text_window.grid(row=15, column=0)

frequency_text_Label.grid(row=16, column=0)
frequency_text_window.grid(row=17, column=0)

cycles_text_Label.grid(row=18, column=0)
cycles_text_window.grid(row=19, column=0)

# column 1

startx.grid(row=0, column=1)

E_O_Label.grid(row=4, column=1)
E_O_Entry.grid(row=5, column=1) #pady=20 to change button distances

O_Duration_Label.grid(row=6, column=1)
O_Duration_Entry.grid(row=7, column=1)

time_between_trains_label.grid(row=8, column=1) 
time_between_trains_entry.grid(row=9, column=1)

pulse_num_label.grid(row=10, column=1) 
pulse_num_entry.grid(row=11, column=1) 

Time_between_pulses_label.grid(row=12, column=1)
Time_between_pulses_entry.grid(row=13, column=1)

run_x_times_label.grid(row=14, column=1)
run_x_times_entry.grid(row=15, column=1)

# column 2
text_Label.grid(row=4, column=2)
text_window.grid(row=5, column=2)

text_1_Label.grid(row=6, column=2)
text_1_window.grid(row=7, column=2)




root.mainloop()


# In[ ]:


# In[ ]:




