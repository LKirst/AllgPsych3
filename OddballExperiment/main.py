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

# set up the directory
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)


expClock = core.Clock()

# -----------------------------------------------------------------------------
# |          Session Data Dlg                                                 |
# -----------------------------------------------------------------------------

exp_dict_dlg = {'Probandennummer':'', 'nTrials':300, 'pDeviant':.18, 'seed':1}
infoDlg = gui.DlgFromDict(exp_dict_dlg, title='Oddball Beispiel', order = ['Probandennummer', 'nTrials', 'seed'])
if not infoDlg.OK: core.quit() # user pressed cancel

# Add some entries
exp_dict_dlg.update({'Version_psychopy': psyvers, 'experimentStart': data.getDateStr(format='%d_%m_%y_%H_%M_%S')})

# output files
datfilename = _thisDir + os.sep + 'testdata' + os.sep + 'VP{}_{}'.format(exp_dict_dlg['Probandennummer'], data.getDateStr())
logfilename = _thisDir + os.sep + 'testdata' + os.sep + 'VP{}_{}_logfile'.format(exp_dict_dlg['Probandennummer'], data.getDateStr())

# logging
logging.console.setLevel(logging.WARNING)  # receive ERROR, but not WARNING, DATA, EXP, INFO or DEBUG in the console
logDat = logging.LogFile(logfilename,
        filemode='w',  # if you set this to 'a' it will append instead of overwriting
        level=logging.EXP)  # errors, warnings, data and exp will be sent to this logfile

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
        stopIndxForInstr    = -1, 
        seed                = exp_dict_dlg['seed'] # make the pseudorandom sequence reproducible
        )

# instruction oddball
myOddball.instruction()

# run oddball
myOddball.runOddball(triggerdeviant = 1, triggerstandard = 2, stopIndex = -1, 
                     waitbeforecontinue = 3)


# input oddball second half
myOddball.inputCount()

# save and abort
thisExp.saveAsWideText(datfilename + '.csv')
thisExp.abort()
win.close()



