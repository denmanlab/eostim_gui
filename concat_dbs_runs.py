#!/usr/bin/env python
# coding: utf-8

# In[1]:


#general imports
import os,sys,glob
import numpy as np
import pandas as pd
import h5py


# In[2]:


# insert Path where recording csv files are saved 
path = '/Users/granthughes/Desktop/Denman_lab/dbs_files/dbs_dataframes/11_10_21/*'

get_ipython().system('ls glob.glob(str(path))')


# In[3]:


# Sort each run's DataFrame by the time
def sort_dbs_runs(paths):
    new_names = []
    for path in paths:
        session_time_string = os.path.basename(path).split('_')[-1]
        if len(session_time_string.split('_')[-1]) < 2:
            hour = '0'+ session_time_string.split('_')[-1]
        else: hour = session_time_string.split('_')[-1]
        if len(session_time_string.split('-')[0]) < 2:
            minute = '0'+ session_time_string.split('-')[0]
        else: minute = session_time_string.split('-')[0]
        if len(session_time_string.split('-')[1]) < 2:
            second = '0'+ session_time_string.split('-')[1]
        else: second = session_time_string.split('-')[1]
#         os.path.basename(path).split('-')[0]+'-'+
        new_names.extend([hour+'_'+minute+'_'+second])
    return np.array(paths)[np.argsort(new_names).astype(int)]
    return new_names
   


# In[4]:


# run sorting function 
sorted_dbs_runs = sort_dbs_runs(glob.glob(path))


# In[5]:


print(sorted_dbs_runs)


# In[6]:


concat_df = pd.concat([pd.read_csv(runs) for runs in sorted_dbs_runs])


# In[7]:


concat_df.head(10)


# In[ ]:




