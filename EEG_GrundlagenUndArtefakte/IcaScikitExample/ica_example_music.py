# -*- coding: utf-8 -*-
"""
Created on Mon May 11 2020

Written by Lukas Kirst on the basis of examples provided by the authors 
of scikit-learn

"""

import numpy as np

import soundfile as sf
import sounddevice as sd

from sklearn.decomposition import FastICA

import os
from pathlib import Path

# Get the data folder (only works if you downloaded the entire project, 
# including the Data folder)
scripts_folder       = Path(__file__).parent.parent.parent
data_folder_expanded = os.path.join(scripts_folder, 'Data')
assert os.path.isdir(data_folder_expanded), ('There is no Data folder '
    'where the script assumes there should be one. You could try setting the '
    'data_folder_expanded variable manually to the folder where you saved the data.')  
os.chdir(data_folder_expanded) # set the working directory

# The ICA is not deterministic; so to make sure that we all get the same results
# We tell numpy to pick the same pseudo-random numbers for us
np.random.seed(0) 

# %% The music

s1, samplerate = sf.read('IntroForTheLongestTime-01.wav')
# sd.play(s1, samplerate)

s2, samplerate = sf.read('IntroForTheLongestTime-02.wav')
# sd.play(s2, samplerate)

# play the two sounds together
sd.play(s1 + s2, samplerate)

# %% Standardize

S = np.c_[s1, s2] # concatenate the signals to one matrix

S /= S.std(axis=0)  # Standardize data

# %% Mix data

# this corresponds to three microphones and the weightings correspond to how
# near the microphones are to the signal
A = np.array([[1, 1], [0.5, 2], [0.8, 0.2]])  # Mixing matrix
X = np.dot(S, A.T)  # Generate observations

# For example the third microphone:
# Because we standardized above, I multiply the recording by 0.3 to stay within
# the range of my speakers :D
sd.play(X[:, 2]*0.3, samplerate)

# %% Compute ICA

ica = FastICA(n_components=2)
S_ = ica.fit_transform(X)  # Reconstruct signals
A_ = ica.mixing_  # Get estimated mixing matrix

# %% Play ICs

# I multply by 10, because the resulting IC is not loud enough
sd.play(S_[:, 1]*10, samplerate)




