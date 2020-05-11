# -*- coding: utf-8 -*-
"""
Created on Mon May 11 10:40:15 2020

@author: Lukas Kirst

Normally I wouldn't interpolate this channel. This is just for illustration
purposes!

"""

import os
import mne
from pathlib import Path

# Open plots in a dedicated matplotlib qt window:
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

# %%

raw.plot()

print(raw.info['bads'])

# %% 

if 'M1' in raw.info['ch_names']: raw.drop_channels(['M1', 'M2'])
biosemi64_montage = mne.channels.make_standard_montage('biosemi64')
raw.set_montage(biosemi64_montage)

# Plot the montage 
biosemi64_montage.plot(kind = 'topomap') # in 2d

# %%

surrounding_chans = ['P7', 'P5', 'PO7', 'PO3', 'O1']
surrounding_chans_ind = [i for i, chan in enumerate(raw.info['ch_names']) 
                         if chan in surrounding_chans]

raw_interpolated = raw.copy().interpolate_bads(reset_bads = False)

for title, data in zip(['before interp', 'after interp'], [raw, raw_interpolated]):
    # with butterfly mode, we plot all channels on top of each other 
    fig = data.plot(butterfly = True, order = surrounding_chans_ind,
                    bad_color = 'r') 
    fig.suptitle(title)

