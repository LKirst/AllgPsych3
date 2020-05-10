"""
Find ECG artifacts

Authors: Alexandre Gramfort <alexandre.gramfort@inria.fr>
         Lukas Kirst

License: BSD (3-clause)

"""

import numpy as np

import mne
from mne import io
from mne.datasets import sample

print(__doc__)

# Open plots in a dedicated matplotlib qt window:
get_ipython().run_line_magic('matplotlib', 'qt')

# %% Load the data

# Path to the sample_audvis_raw file
data_path = sample.data_path()
raw_fname = data_path + '/MEG/sample/sample_audvis_raw.fif'

# Setup for reading the raw data
raw_sample = io.read_raw_fif(raw_fname)

# %% Create ECG events based on an MEG ECG channel

ecg_event_id = 999
ecg_events, _, _ = mne.preprocessing.find_ecg_events(raw_sample, ecg_event_id,
                                                     ch_name='MEG 1531')

print("Number of detected ECG artifacts : %d" % len(ecg_events))

# %% Plot the sensor locations and the channel "EEG 060"

raw_sample.plot_sensors(ch_type='eeg')

# EEG 060 is at index 374
raw_sample.plot(events = ecg_events, order = [374], n_channels = 1)

# %% Create ECG-epochs for EEG data

# Read epochs
picks = mne.pick_types(raw_sample.info, meg=False, eeg=True, stim=False, eog=False,
                       exclude='bads')
tmin, tmax = -0.1, 0.1
raw_sample.del_proj()
ecg_epochs = mne.Epochs(raw_sample, 
                    events = ecg_events, 
                    ecg_event_id = ecg_event_id, 
                    tmin = tmin, 
                    tmax = tmax, 
                    picks=picks)

ecg_epochs.plot(picks=['EEG 060', 'EEG 036', 'EEG 058', 'EEG 057', 'EEG 043', 'EEG 044'])

# %% Average ECG epochs

avg_ecg_epochs = ecg_epochs.average()

avg_ecg_epochs.plot()

topomap_ecg = avg_ecg_epochs.plot_topomap(times=np.linspace(-0.05, 0.05, 11))
# topomap_ecg.savefig('topomap_ecg.png')



