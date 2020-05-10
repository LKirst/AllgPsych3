"""
==================
Find EOG artifacts
==================

Locate peaks of EOG to spot blinks and general EOG artifacts.

Authors: Alexandre Gramfort <alexandre.gramfort@inria.fr>
         Lukas Kirst

License: BSD (3-clause)

"""

import numpy as np
import matplotlib.pyplot as plt

import mne
from mne import io
from mne.datasets import sample

print(__doc__)

# Open plots in a dedicated matplotlib qt window:
get_ipython().run_line_magic('matplotlib', 'qt')

# %% Load the data

# You don't need to run this cell if you've already loaded the sample data in
# another script!

data_path = sample.data_path()
raw_fname = data_path + '/MEG/sample/sample_audvis_filt-0-40_raw.fif'

# Setup for reading the raw data
raw_sample = io.read_raw_fif(raw_fname)

# %% Find EOG-artifacts based on an EOG channel

eog_event_id = 998
eog_events = mne.preprocessing.find_eog_events(raw_sample, eog_event_id)

print("Number of detected EOG artifacts : %d" % len(eog_events)) 

# %% Plot the sensor locations and the continuous raw data

raw_sample.plot_sensors(ch_type='eeg')

# the indeces correspond to the frontal electrodes and the EOG channel
raw_sample.plot(events = eog_events, 
                order = np.hstack((np.arange(315, 331), 375)),
                n_channels = 17)

# %% Make EOG epochs

picks = mne.pick_types(raw_sample.info, meg=False, eeg=True, stim=False, eog=False,
                       exclude='bads')
tmin, tmax = -0.2, 0.2
eog_epochs = mne.Epochs(raw_sample, eog_events, eog_event_id, tmin, tmax, picks=picks)

eog_epochs.plot()

# %% Average EOG eopochs

avg_eog_epochs = eog_epochs.average()

avg_eog_epochs.plot()

topomap_eog = avg_eog_epochs.plot_topomap(times=np.linspace(-0.2, 0.2, 11))
# topomap_eog.savefig('topomap_eog.png')

# avg_eog_epochs.plot_joint()







