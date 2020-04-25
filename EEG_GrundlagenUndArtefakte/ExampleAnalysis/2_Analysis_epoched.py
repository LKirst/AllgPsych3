# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 12:39:02 2020

@author: LKirst
"""

import os
import mne

# Open plots in a dedicated matplotlib qt window:
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

# %% Find events 

events = mne.find_events(raw, stim_channel = 'Status')
# 41 is the deviant
# 42 is the standard

print(events[np.isin(events[:,2], [41, 42])])

# %% Creating an epochs object and rejecting epochs based on µV-Threshold

event_dict = {'standard': 31, 'target': 32}

reject_criteria = dict(eeg=150e-6,   # 150 µV
                       eog=250e-6)   # 250 µV

epochs = mne.Epochs(raw, events, event_id=event_dict, tmin=-0.2, tmax=0.5,
                    reject=reject_criteria, preload=True)

epochs.plot_drop_log()

# %% ICA

ica = mne.preprocessing.ICA(n_components=20, random_state=97, max_iter=800)
ica.fit(raw)
ica.exclude = [1, 2]  # details on how we picked these are omitted here
ica.plot_properties(raw, picks=ica.exclude)