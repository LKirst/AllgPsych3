# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 01:52:23 2020

@author: Lukas Kirst

In diesem Tutorial zeige ich euch, wie Sinusoide kombiniert werden koennen, 
zu einer komplexeren Sinusoiden.

"""

import numpy as np
from scipy import  fftpack
import matplotlib.pyplot as plt

# If you want to see the plots in a dedicated matplotlib window:
get_ipython().run_line_magic('matplotlib', 'qt')

# %%

fig, axes = plt.subplots(nrows = 4, sharex = True, sharey = True) 

time_step = 0.02
x = np.arange(0, 20, time_step) # a time vector

# %% Three sinusoids

# 2*pi/period is the length of one cycle

period_y1   = 1
ampl_y1     = 2
y1          = ampl_y1*np.sin(2*np.pi*period_y1*x)

period_y2   = 3
ampl_y2     = 1
y2          = ampl_y2*np.sin(2*np.pi*period_y2*x)


period_y3   = 8
ampl_y3     = 2
y3          = ampl_y3*np.sin(2*np.pi*period_y3*x)


# %% Sum sinusoids

sig = y1+y2+y3

axes[0].plot(x, y1, color='b', lw=2)
axes[1].plot(x, y2, color='g', lw=2)
axes[2].plot(x, y3, color='y', lw=2)
axes[3].plot(x, sig, color='r', lw=2)

axes[0].set_xlim(0, 2)
axes[3].set_xlabel('time')

fig.show()

# %% Fourier transform

fig, ax = plt.subplots()

# FFT of the signal
sig_fft = fftpack.fft(sig)

# Power of the signal
power = np.abs(sig_fft)

# Frequencies
sample_freq = fftpack.fftfreq(sig.size, d = time_step)

# Plot
ax.plot(sample_freq, power)
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Power')
ax.set_xlim(0, 20)




