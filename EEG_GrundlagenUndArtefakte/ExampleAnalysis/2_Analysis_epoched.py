# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 12:39:02 2020

@author: Lukas Kirst
"""

import os
import mne
import numpy as np

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

# We have a biosemi system
biosemi64_montage = mne.channels.make_standard_montage('biosemi64')
raw.set_montage(biosemi64_montage, raise_if_subset = False)

# %% Find events 

events = mne.find_events(raw, stim_channel = 'Status')
# 41 is the deviant
# 42 is the standard

print(events[np.isin(events[:,2], [41, 42])])

# %% Creating an epochs object and rejecting epochs based on µV-Threshold

event_dict = {'deviant': 41, 'standard': 42}

reject_criteria = dict(eeg=200e-6) # 150 µV

epochs = mne.Epochs(raw, events, event_id=event_dict, tmin=-0.2, tmax=0.5,
                    reject=reject_criteria, preload=True, 
                    baseline = (-0.2, 0),
                    picks = raw.ch_names[0:63])

epochs.plot_drop_log()

# %% Run ICA

# ICA has a random component. We specify a random seed so that we get 
# identical results every time the analysis is run
ica = mne.preprocessing.ICA(n_components=20, random_state=99, max_iter=800)
ica.fit(epochs)

# Plot the ICs
ica.plot_sources(epochs)

# %%

# Plot an overlay of the original signal against the reconstructed signal with
# the artefactual ICs excluded
ica.plot_components(inst = epochs)

# %% exclude components

ica.exclude = [1, 2]  # details on how we picked these are omitted here
ica.plot_properties(epochs, picks=ica.exclude)











