#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

@author: LKirst

Psychpy v3.0
Python 3.6

"""

import os

from psychopy import data, visual, logging, gui, core
from psychopy import __version__ as psyvers

import oddball

logging.console.setLevel(logging.DEBUG)

expClock = core.Clock()

# -----------------------------------------------------------------------------
# |          Session Data Dlg                                                 |
# -----------------------------------------------------------------------------

exp_dict_dlg = {'Probandennummer':'', 'nTrials':300, 'pDeviant':.2}
infoDlg = gui.DlgFromDict(exp_dict_dlg, title='Oddball Beispiel', order = ['Probandennummer', 'nTrials'])
if not infoDlg.OK: core.quit() # user pressed cancel

# Add some entries
exp_dict_dlg.update({'Version_psychopy': psyvers, 'experimentStart': data.getDateStr(format='%d_%m_%y_%H_%M_%S')})


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

nTrials = exp_dict_dlg['nTrials']

# initialise an Oddball object
myOddball = oddball.Oddball(
        win         = win, 
        expHandler  = thisExp, 
        mydir       = _thisDir, 
        subjectnr   = exp_dict_dlg['Probandennummer'], 
        sessionnr   = '1', 
        triggerlen  = 0.01,
        ntrials             = nTrials, # number of trials
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
        stopIndxForInstr    = nTrials/2-1
        )

# instruction oddball
myOddball.instruction(captureScreenshot = True)
myOddball.saveScreenshot()

# run and time first half of oddball
myOddball.runOddball(triggerdeviant = 1, triggerstandard = 2, stopIndex = nTrials/2-1, waitbeforecontinue = 3)

# input oddball first half
myOddball.inputCount()

# instruction reminder
myOddball.reminder()

# run second half of oddball and ask for input
myOddball.runOddball(triggerdeviant = 1, triggerstandard = 2, stopIndex = -1, waitbeforecontinue = 0)

# input oddball second half
myOddball.inputCount()

# save and abort
thisExp.saveAsWideText(datfilename + '.csv')
thisExp.abort()
win.close()



