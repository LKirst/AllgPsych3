# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 12:39:02 2020

@author: Lukas Kirst
"""

import os
import mne
import numpy as np
import matplotlib.pyplot as plt

# Open plots in a dedicated matplotlib qt window:
get_ipython().run_line_magic('matplotlib', 'qt')

# %% Loading the raw data

# N.b.: don't use single backward slashes in your path.
# On Windows, if you copy a path, you have to replace every single backslash \
# with either a forward slash / or a double backslash \\
data_folder_expanded = 'C:/Users/sls13204/Documents/AllgPsyVI/Lehre/Allgemeine3/Daten' 

data_filename = 'LK_1_post1'
data_filepath_raw = os.path.join(data_folder_expanded, 
                                 data_filename + '_cropped_raw.fif')

raw = mne.io.read_raw_fif(data_filepath_raw, preload = True)

# We have a biosemi system
biosemi64_montage = mne.channels.make_standard_montage('biosemi64')
if 'M1' in raw.info['ch_names']: raw.drop_channels(['M1', 'M2']) # set_montage raises an error if M1 or M2 are still in the data
raw.set_montage(biosemi64_montage)

# %% Find events 

events = mne.find_events(raw, stim_channel = 'Status')

# 41 is the deviant; 42 is the standard
event_dict = {'deviant': 41, 'standard': 42}

print(events[np.isin(events[:,2], [41, 42])])

fig, ax1 = plt.subplots()
mne.viz.plot_events(events, sfreq=raw.info['sfreq'], 
                          event_id=event_dict, axes = ax1,
                          first_samp = raw.first_samp)
fig.show()


# %% Creating an epochs object and rejecting epochs based on µV-Threshold

reject_criteria = dict(eeg=200e-6) # 200 µV

epochs = mne.Epochs(raw, events, event_id=event_dict, tmin=-0.2, tmax=0.5,
                    reject=reject_criteria, preload=True, 
                    baseline = (-0.2, 0),
                    picks = raw.ch_names[0:63])

epochs.plot_drop_log()

# %% Run ICA

# ICA has a random component. We specify a random seed so that we get 
# identical results every time the analysis is run
ica = mne.preprocessing.ICA(max_pca_components = 20, random_state=99, max_iter=800)
ica.fit(epochs)

# Plot the ICs
ica.plot_sources(epochs)

# %% Show properties of ICs

# Plot an overlay of the original signal against the reconstructed signal with
# the artefactual ICs excluded
ica.plot_components(inst = epochs, psd_args = {'fmax':50})

# %% exclude components

ica.exclude = [2, 9, 10]
ica.plot_properties(epochs, picks=ica.exclude, psd_args = {'fmax':50})

epochs_ICs_rejected = epochs.copy()
ica.apply(epochs_ICs_rejected)

# %% average

evoked = epochs_ICs_rejected.average()

# %% save

data_filepath_evoked = os.path.join(data_folder_expanded, data_filename + 
                                      '_ave.fif')

evoked.save(data_filepath_evoked)











