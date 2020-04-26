# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 16:52:37 2020

@author: Lukas Kirst

Tutorial to illustrate filters.

"""


import os
import mne
import matplotlib.pyplot as plt

# %%

# If you want to see the plots in a dedicated matplotlib window:
get_ipython().run_line_magic('matplotlib', 'qt')

# %% Loading the raw data

# N.b.: don't use single backward slashes in your path.
# On Windows, if you copy a path, you have to replace every single backslash \
# with either a forward slash / or a double backslash \\
data_folder = '~\\Documents\\AllgPsyVI\\Lehre\\Allgemeine3\\Daten' 
data_folder_expanded = os.path.expanduser(data_folder) # this expands the tilde to contain the path of my windows user

data_filename = 'LK_1_post1'
data_filepath_raw = os.path.join(data_folder_expanded, 
                                 data_filename + '_cropped_raw.fif')

raw = mne.io.read_raw_fif(data_filepath_raw, preload = True) 

# We have a biosemi system
biosemi64_montage = mne.channels.make_standard_montage('biosemi64')
raw.set_montage(biosemi64_montage, raise_if_subset = False)

# %% High-pass

filt_hp_raw = raw.copy().filter(l_freq = 0.1, h_freq = None) 
# filt_hp_raw.plot()
# filt_hp_raw.plot_psd()

# %% Low-pass

filt_lp_raw = raw.copy().filter(l_freq = None, h_freq = 40) 
# filt_lp_raw.plot_psd()

# %% Notch

filt_notch_raw = raw.copy().notch_filter(freqs = 50)
# filt_notch_raw.plot_psd()




