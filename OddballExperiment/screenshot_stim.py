#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

@author: LKirst

Psychpy v2020.1.3
Python 3.6

"""

import oddball



import os

from psychopy import data, visual, logging, gui, core
from psychopy import __version__ as psyvers

import oddball

logging.console.setLevel(logging.DATA)

expClock = core.Clock()

# -----------------------------------------------------------------------------
# |          Session Data Dlg                                                 |
# -----------------------------------------------------------------------------

exp_dict_dlg = {'Probandennummer':'', 'nTrials':300, 'pDeviant':.2, 'Probandennummer': 99, 
    'Version_psychopy': psyvers, 'experimentStart': data.getDateStr(format='%d_%m_%y_%H_%M_%S')}

# -----------------------------------------------------------------------------
# |          Initialising Objects                                             |
# -----------------------------------------------------------------------------


win = visual.Window(
                    [1280*0.7, 1024*0.7], # 70% of the size of the screen in WH205
                    fullscr=True,
                    allowGUI=False,
                    monitor='testMonitor',
                    units='cm'
                    )
_thisDir    = os.path.dirname(os.path.abspath(__file__))
datfilename = _thisDir + os.sep + 'testdata/odballData'

thisExp = data.ExperimentHandler(
                                name= '',
                                version='',
                                extraInfo= exp_dict_dlg,
                                runtimeInfo=None,
                                originPath=None,
                                dataFileName=datfilename,
                                savePickle=True,
                                saveWideText=True,
                                autoLog=True
                                )

# initialise an Oddball object
myOddball = oddball.Oddball(
        win         = win, 
        expHandler  = thisExp, 
        mydir       = _thisDir, 
        subjectnr   = exp_dict_dlg['Probandennummer'], 
        sessionnr   = '1', 
        triggerlen  = 0.01,
        ntrials             = 300, # number of trials
        nfr_on2onisi_upper  = 150, # upper bound of isis in frames
        nfr_on2onisi_lower  = 126, # lower bound of isis in frames
        nFrStim             = 6, # length of stimulus presentation in frames
        pdeviants           = exp_dict_dlg['pDeviant'], # probability of deviants
        maxNConsecStan      = 31, # the array that determines whether a stimulus is a deviant or a standard is divided 
                            # in pairs, each containing a deviant in first place and a standard or deviant in second place
                            # max(diffPairsIndeces) > int((maxNConsecStan)/2) the list of pairs will be reshuffled
        verticesPixStim     = [(-20,-20),(-20,20),(20,20),(20,-20)], # the vertices of the shape in pixels
        trackFrIntervals    = True,
        dataSaveClock       = expClock,
        stopIndxForInstr    = -1, 
        seed                = 0 # make the pseudorandom sequence reproducible
        )


myOddball.drawStimForScreenshot()


thisExp.abort()
win.close()
