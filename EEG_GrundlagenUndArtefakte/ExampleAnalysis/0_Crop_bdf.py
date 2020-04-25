# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 09:49:14 2020

@author: LKirst

In this file, I crop the data file to the part, which is relevant for the 
example analysis.

"""

import os
import mne
import numpy as np

# %% Loading the raw data

# N.b.: don't use single backward slashes in your path.
# On Windows, if you copy a path, you have to replace every single backslash \
# with either a forward slash / or a double backslash \\
data_folder = '~\\Documents\\AllgPsyVI\\Lehre\\Allgemeine3\\Daten' 
data_folder_expanded = os.path.expanduser(data_folder) # this expands the tilde to contain the path of my windows user

data_filename = 'LK_1_post1'
data_filepath_raw = os.path.join(data_folder_expanded, data_filename + '.bdf')

raw = mne.io.read_raw_bdf(data_filepath_raw, preload = True) 

# %% Find events

events = mne.find_events(raw, stim_channel = 'Status')

events_relevant = events[np.isin(events[:,2], [41, 42])]

t_event_first = min(events_relevant[:,0])/raw.info['sfreq']
t_event_last  = max(events_relevant[:,0])/raw.info['sfreq']

print('The range you are interested starts at t = {} and ends at t = {}'.format(
    t_event_first,
    t_event_last
    ))


# %% Crop the data

# Add 3 secs at the start and at the end
t_file_start = t_event_first + 4
t_file_end   = t_event_last + 4  

raw.crop(tmin = t_file_start, tmax = t_file_end)

# %% Rename the mastoids and remove irrelevant sensors

# Rename the mastoids
raw.rename_channels(mapping = {'EXG5':'M1', 'EXG6':'M2'})

# We're only interested in EEG channels, so we can exclude other channels
raw.pick(picks = 'all', exclude = [
    'EXG1', 'EXG2', 'EXG3', 'EXG4', 'EXG7', 'EXG8', 
    'GSR1', 'GSR2', 
    'Erg1', 'Erg2', 
    'Resp', 'Plet', 'Temp'
    ])

# %% Save

data_filepath_filtered = os.path.join(data_folder_expanded, data_filename + 
                                      '_cropped_raw.fif')

raw.save(data_filepath_filtered, overwrite=True)

