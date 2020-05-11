# -*- coding: utf-8 -*-
"""
Written by the authors of MNE-Python, modified by Lukas Kirst

Source of the original file: 
    https://github.com/mne-tools/mne-python/blob/master/tutorials/preprocessing/plot_55_setting_eeg_reference.py

License: BSD (3-clause)

In diesem Tutorial wird euch demonstriert, welchen Einfluss die Wahl einer
Referenzelektrode auf die Daten hat. Dafür rereferenzieren wir die Daten mit 
unterschiedlichen Referenzelektroden.

Wenn ihr vom Skript 1_Analysis_raw.py kommt koennt ihr den Abschnitt, in dem
die Daten geladen werden ("Loading the raw data") ueberspringen!

"""

import os
import mne
import matplotlib.pyplot as plt
from pathlib import Path

# If you want to see the plots in a dedicated matplotlib window:
get_ipython().run_line_magic('matplotlib', 'qt')

# Get the data folder (only works if you downloaded the entire project, 
# including the Data folder)
scripts_folder       = Path(__file__).parent.parent.parent
data_folder_expanded = os.path.join(scripts_folder, 'Data')
assert os.path.isdir(data_folder_expanded), ('There is no Data folder '
    'where the script assumes there should be one. You could try setting the '
    'data_folder_expanded variable manually to the folder where you saved the data.')

# %% Loading the raw data

data_filename = 'LK_1_post1'
data_filepath_raw = os.path.join(data_folder_expanded, 
                                 data_filename + '_cropped_raw.fif')

raw = mne.io.read_raw_fif(data_filepath_raw, preload = True) 

# We have a biosemi system
biosemi64_montage = mne.channels.make_standard_montage('biosemi64')
raw.set_montage(biosemi64_montage, raise_if_subset = False)


# %% Background

# EEG measures a voltage (difference in electric potential) between each
# electrode and a reference electrode. This means that whatever signal is
# present at the reference electrode is effectively subtracted from all the
# measurement electrodes. Therefore, an ideal reference signal is one that
# captures *none* of the brain-specific fluctuations in electric potential,
# while capturing *all* of the environmental noise/interference that is being
# picked up by the measurement electrodes.
#
# In practice, this means that the reference electrode is often placed in a
# location on the subject's body and close to their head (so that any
# environmental interference affects the reference and measurement electrodes
# similarly) but as far away from the neural sources as possible (so that the
# reference signal doesn't pick up brain-based fluctuations). Typical reference
# locations are the subject's earlobe, nose, mastoid process, or collarbone.
# Each of these has advantages and disadvantages regarding how much brain
# signal it picks up (e.g., the mastoids pick up a fair amount compared to the
# others), and regarding the environmental noise it picks up (e.g., earlobe
# electrodes may shift easily, and have signals more similar to electrodes on
# the same side of the head).
#
# Even in cases where no electrode is specifically designated as the reference,
# EEG recording hardware will still treat one of the scalp electrodes as the
# reference, and the recording software may or may not display it to you (it
# might appear as a completely flat channel, or the software might subtract out
# the average of all signals before displaying, making it *look like* there is
# no reference).

# Here's how the data looks in its original state:

raw.plot()

# add new reference channel (all zero); this function returns a copy
raw_new_ref = mne.add_reference_channels(raw, ref_channels=['EEG 999'])


# %% Rereference to linked mastoids

raw_linkedmastoids = raw_new_ref.set_eeg_reference(ref_channels=['M1', 'M2'])

raw_linkedmastoids.plot()


# %% Average reference
# The average reference is a virtual reference that is the average of all channels.

raw_avg_ref = raw.copy().set_eeg_reference(ref_channels='average')

raw_avg_ref.plot()


# %% Try out a different reference electrode to test the effect of referencing

exercise_ref_chan = ['O1']
raw_exercise = raw.copy().set_eeg_reference(ref_channels=['O1'])

raw_exercise.plot()

# %% Plot psd 

fig, axes = plt.subplots(nrows = 2, ncols = 2, sharey = True, sharex = True)

axes = axes.flatten()

for i, (title, raw_obj, exclude) in enumerate([
        ('Before re-ref',                       raw, None), 
        ('Linked mastoids',                     raw_linkedmastoids, ['M1', 'M2']),
        ('Avg reference',                       raw_avg_ref, None),
        ('Re-ref to ' + exercise_ref_chan[0],   raw_exercise, ['Fp1'])
        ]):
    
    # exclude the reference channels (they should not show oscillations)
    if exclude is not None:
        picks = [chan for chan in raw_obj.ch_names if chan not in exclude]
    else:
        picks = raw_obj.ch_names
    
    raw_obj.plot_psd(fmax = 70, ax = axes[i], picks = picks)
    axes[i].set_title(title)



# %% Plot evoked data

events = mne.find_events(raw, stim_channel = 'Status')
event_dict = {'deviant': 41, 'standard': 42}
epochs_params = dict(events=events, event_id=event_dict['deviant'], 
                     tmin=-0.2, tmax=0.6,
                     picks= 'all')

fig_evok, axes_evok = plt.subplots(nrows = 2, ncols = 2, sharey = True, sharex = True)
axes_evok = axes_evok.flatten()

for i, (title, raw_obj) in enumerate([
        ('Before re-ref',                       raw), 
        ('Linked mastoids',                     raw_linkedmastoids),
        ('Avg reference',                       raw_avg_ref),
        ('Re-ref to ' + exercise_ref_chan[0],   raw_exercise)
        ]):

    evoked_Pz = mne.Epochs(raw_obj, **epochs_params).average()
    evoked_Pz.plot(axes = axes_evok[i])
    axes_evok[i].set_title(title)
    








