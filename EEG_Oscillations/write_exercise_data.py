# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 00:51:05 2020

@author: Lukas Kirst
"""

import numpy as np
import os

# set the working directory
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)


# %% Exercise 1

x1 = np.linspace(0, 4, 1000) # a time vector

freq_y1     = 0.5
period_y1   = 1/freq_y1
ampl_y1     = 2
y1          = ampl_y1*np.sin(2*np.pi/period_y1*x1)

freq_y2     = 3.3
period_y2   = 1/freq_y2
ampl_y2     = 1
y2          = ampl_y2*np.sin(2*np.pi/period_y2*x1)

freq_y3     = 15
period_y3   = 1/freq_y3
ampl_y3     = 0.3
y3          = ampl_y3*np.sin(2*np.pi/period_y3*x1)

# add the three sine waves to get the signal
signal1 = y1 + y2 + y3


# %% Exercise 3

x2 = np.linspace(0, 1, 1000) # a time vector

freq_y4     = 2
ampl_y4     = 1
y4          = ampl_y4*np.sin(2*np.pi*freq_y4*x2)
weights_y4  = -5*x2+5 # weigh the amplitude by the linear function -5*x+5

freq_y5     = 20
ampl_y5     = 1
y5          = ampl_y5*np.sin(2*np.pi*freq_y5*x2)
weights_y5  = np.concatenate(
    (5*x2[0:500]+0.5,
    -5*x2[500:1000]+5.5), 
    axis = None)

signal2 = y4*weights_y4 + y5*weights_y5

# %% Save

with open('data_exercise1.npy', 'wb') as f:
    np.save(f, x1)
    np.save(f, signal1)

with open('data_exercise2.npy', 'wb') as f:
    np.save(f, x2)
    np.save(f, signal2)






