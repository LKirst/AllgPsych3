# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 21:35:47 2020

@author: Lukas Kirst

"""


import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
import os

# If you want to see the plots in a dedicated matplotlib window:
get_ipython().run_line_magic('matplotlib', 'qt')

# set the working directory
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# %% Exercise 1

with open('data_exercise1.npy', 'rb') as f:
    x1 = np.load(f)
    signal1 = np.load(f)

# plot
fig, axes = plt.subplots(nrows = 1, figsize=(9, 5)) 
axes.plot(x1, signal1)
axes.grid(True)

axes.set_ylabel('voltage(mV)')
axes.set_xlabel('time (secs)')

fig.savefig('exercise1.png')

#%% Exercise 3

with open('data_exercise2.npy', 'rb') as f:
    x2 = np.load(f)
    signal2 = np.load(f)

# plot
fig2, axes2 = plt.subplots(nrows = 3, 
                           figsize=(8,12),
                           sharex = True) 
axes2[0].plot(x2, signal2)
# axes2[1].plot(x2, weights_y4)
# axes2[2].plot(x2, weights_y5)
for ax in axes2: 
    ax.grid(True)
    ax.set_ylabel('voltage(mV)')
    ax.set_xlabel('time(secs)')
    ax.xaxis.set_tick_params(which = 'both', labelbottom = True)

axes2[0].set_yticks(np.arange(-6, 6, 2))

for i in [1,2]:
    axes2[i].set_ylim((0,5))
    axes2[i].set_title(f'Frequenz {i} ( ___ Hz)')

fig2.tight_layout(pad = 4)

fig2.savefig('exercise3.png')


# %% Fourier transform

for x, sig, title in [(x1, signal1, 'Exercise 1'), (x2, signal2, 'Exercise 2')]:
    fig, ax = plt.subplots()
    
    # FFT of the signal
    sig_fft = fftpack.fft(sig)
    
    # Power of the signal
    power = np.abs(sig_fft)
    
    # Frequencies
    sample_freq = fftpack.fftfreq(sig.size, d = x[1]-x[0])
    
    # Plot
    ax.plot(sample_freq, power)
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Power')
    ax.set_xlim(0, 25)
    ax.set_title(title)
















