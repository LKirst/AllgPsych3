# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 12:39:02 2020

@author: LKirst
"""

import os
import mne

# Open plots in a dedicated matplotlib qt window:
get_ipython().run_line_magic('matplotlib', 'qt')


# %% Detecting events

events = mne.find_events(filt_raw, stim_channel='STI 014')
print(events[:5])  # show the first 5

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