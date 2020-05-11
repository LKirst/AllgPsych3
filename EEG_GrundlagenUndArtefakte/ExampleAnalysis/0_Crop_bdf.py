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
from pathlib import Path

# Get the data folder (only works if you downloaded the entire project, 
# including the Data folder)
scripts_folder       = Path(__file__).parent.parent.parent
data_folder_expanded = os.path.join(scripts_folder, 'Data')
assert os.path.isdir(data_folder_expanded), ('There is no Data folder '
    'where the script assumes there should be one. You could try setting the '
    'data_folder_expanded variable manually to the folder where you saved the data.')

# %% Loading the raw data

data_filename = 'LK_1_post1'
data_filepath_raw = os.path.join(data_folder_expanded, data_filename + '.bdf')

raw = mne.io.read_raw_bdf(data_filepath_raw, preload = True) 


# %% Find events

events = mne.find_events(raw, stim_channel = 'Status')

events_relevant = events[np.isin(events[:,2], [41, 42])]
t_event_first = min(events_relevant[:,0])/raw.info['sfreq']
t_event_last  = max(events_relevant[:,0])/raw.info['sfreq']

print('The file length in secs is {}'.format(raw.times[-1]))
print('The range you are interested starts at t = {} and ends at t = {}'.format(
    t_event_first,
    t_event_last
    ))

# %% Crop the data

# Add 3 secs at the start and at the end
t_file_start = t_event_first - 4
t_file_end   = t_event_last + 4  

raw_cropped = raw.copy().crop(tmin = t_file_start, tmax = t_file_end)

# %% Rename the mastoids and remove irrelevant sensors

# Rename the mastoids
raw_cropped.rename_channels(mapping = {'EXG5':'M1', 'EXG6':'M2'})

# We're only interested in EEG channels, so we can exclude other channels
raw_cropped.pick(picks = 'all', exclude = [
    'EXG1', 'EXG2', 'EXG3', 'EXG4', 'EXG7', 'EXG8', 
    'GSR1', 'GSR2', 
    'Erg1', 'Erg2', 
    'Resp', 'Plet', 'Temp'
    ])

# %% Save

data_filepath_cropped = os.path.join(data_folder_expanded, data_filename + 
                                      '_cropped_raw.fif')

raw_cropped.save(data_filepath_cropped, overwrite=True)

