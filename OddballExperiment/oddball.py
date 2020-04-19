#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

@author: LKirst

Psychpy v2020.1.3
Python 3.6

"""

from psychopy import data, visual, event, core, logging
from psychopy.constants import (NOT_STARTED, STARTED, STOPPED)

import numpy as np
import csv

import textinput

try:
    from psychopy import parallel
    if parallel.ParallelPort is None:
        import utils_parallel_simulated as parallel
        logging.warn('A parallel port will be simulated!')
    parallel_imported = True
except OSError:
    parallel_imported = False
    logging.warn('The package "parallel" could not be found! No trigger will be sent.')


class Oddball:
    
    def __init__(self, win, expHandler, mydir, subjectnr, sessionnr, triggerlen, 
                    ntrials, # number of Trials
                    nfr_on2onisi_upper, # upper bound of isis in frames
                    nfr_on2onisi_lower, # lower bound of isis in frames
                    nFrStim, # length of stimulus presentation in frames
                    pdeviants, # probability of deviants
                    maxNConsecStan, # the array that determines whether a stimulus is a deviant or a standard is divided 
                                    # in pairs, each containing a deviant in first place and a standard or deviant in second place
                                    # max(diffPairsIndeces) > int((maxNConsecStan)/2) the list of pairs will be reshuffled
                    verticesPixStim, # the vertices of the shape in pixls
                    trackFrIntervals = True, # whether to track the frame intervals
                    dataSaveClock = None, # a clock for which we'll query for the timing of every trial stored alongside the data
                    stopIndxForInstr = -1,
                    seed = None
                    ):
        
        np.random.seed(seed = seed) # if seed is not None, the calls to 
        # np.random will not be (pseudo-)random but produce a reproducible sequence
    
        
        self.win        = win
        self.thisExp    = expHandler
        self.nFrStim    = nFrStim
        self.triggerlen = triggerlen
        self.trackFrIntervals = trackFrIntervals
        
        # check the framerate
        framerate = win.getActualFrameRate()
        logging.warn('The framerate is: %d' %framerate)
        assertWarningTxt = 'The length you set for the presentation of the'\
            ' stimulus is less than the length for which you send a trigger. '\
            'This is not possible.'
        assert self.triggerlen <= self.nFrStim*1/framerate, assertWarningTxt
        
        stims = self._stimsList(ntrials, pdeviants, maxNConsecStan)
        self.isi_list = self._isiList(nfr_on2onisi_lower, nfr_on2onisi_upper, nFrStim, ntrials)
        
        # initialize stimuli
        myOris = [0.0, 45.0] # one of the stimuli will be turned by 45 degrees
        np.random.shuffle(myOris) # returns None!
        self.deviant = visual.ShapeStim(win, units = 'pix', vertices=verticesPixStim, lineWidth=5, ori = myOris[0], name = 'oddball_deviant')
        self.standard = visual.ShapeStim(win, units = 'pix',vertices=verticesPixStim, lineWidth=5, ori = myOris[1], name = 'oddball_standard')
        
        # create a list of dicts with isi and stimtype for every trial
        trialList = []
        for i,j in zip(stims, self.isi_list):
            trialList.append(dict(standard = i, isi = j))
        # initialize a TrialHandler object
        self.trialHandler = data.TrialHandler(
                    trialList= trialList,
                    nReps = 1,
                    method='sequential',
                    extraInfo={'deviant_ori': self.deviant.ori}, # store which shape was the deviant
                    name='trialhandler_oddball'
                    )
        self.thisExp.addLoop(self.trialHandler)
        
        # Initialise a port
        self.parallel_port_exists = False # initialized with False, so that if the parallel port 
        #   cannot be initialised, I later query this variable and avoid running code that would through error without a parallel port
        if parallel_imported:
            try:
                self.port = parallel.ParallelPort(address=0x0378)
                self.parallel_port_exists = True
            except Exception:
                logging.warn('Es konnte kein parallel port initialisiert werden! Es werden keine Trigger gesendet.')
        
        # the text for instruction
        instrString = 'Im Folgenden werden Ihnen in schneller Reihenfolge in '\
            'zwei Blöcken je 150 Formen hintereinander auf dem Bildschirm präsentiert. '\
            'Sie sollen zählen, wie oft Ihnen die Form, die Sie unten '\
            'links sehen, präsentiert wird. Die Form, die Sie unten '\
            'rechts sehen, sollen sie nicht beachten.\n'\
            '\nDrücken Sie die Leertaste, um die ersten {} Formen '\
            'zu sehen.'.format(len(trialList) if stopIndxForInstr is -1 else stopIndxForInstr)
        self.instructionTxt = visual.TextStim(
            win, height =.08, units='norm', pos = (0,0.5), wrapWidth = 1.5,
            text = instrString, name = 'instruction_oddball')
        
        # an object to run a routine which allows entering numbers 
        # without a dlg gui, but directly on screen
        self.textInput = textinput.TextInput(self.win)
        
        # clocks for timing and a mouse to hide the mouse during the trial
        self.trialClock = core.Clock() # this clock is for the timing of triggers
        self.dataSaveClock = core.Clock() if dataSaveClock is None else dataSaveClock # this clock is for storing the time of each trial
        self.mouse = event.Mouse(win = self.win)
    
    def runOddball(self, triggerdeviant, triggerstandard, stopIndex, 
                   waitbeforecontinue = 2):
        """
        The most accurate way to time your stimulus presentation is to
        present for a certain number of frames. For that to work you need
        your window flips to synchronize to the monitor and not to drop
        any frames.
        """
        if (stopIndex+1)%2 != 0:
            logging.error(
                'If (stopIndex+1)%2 != 0, the next call of runOddball could '\
                'start with a deviant and not with a standard, which would '\
                'be preferable!')
        
        if self.trackFrIntervals: self.win.recordFrameIntervals = True
        
        if self.parallel_port_exists and self.port.status == STARTED: # this should never equal true!
            logging.error('port.status should not be STARTED at this point.')
            self.port.status = STOPPED
            self.port.setData(0) # set the trigger back to 0
        
        # centre the stimuli in the middle
        self.deviant.pos = self.standard.pos = (0,0)
        # add the start time to the trial handler
        self.trialHandler.addData('starttime_oddball', 
                                  data.getDateStr(format='%H_%M_%S'))
    
        for thisTrial in self.trialHandler:
            
            # ------------------------------------------------
            # |          Prepare to start trial              |
            # ------------------------------------------------
            frameN = -1 # the first frame in the trial has the index 0
            on2On_isi = thisTrial['isi'] # this is the length of the trial in frames
            off2On_isi = on2On_isi-self.nFrStim # this is the n of frames 
                                                # between the offset of one 
                                                # stimulus and the onset of the next stimulus
            if thisTrial['standard']: # TrialPair['standard'] is 0 or 1 which is the same as False or True
                triggerSignal = triggerstandard
                stim = self.standard
            else:
                triggerSignal = triggerdeviant
                stim = self.deviant
            stim.status = NOT_STARTED
            continueRoutine = True
            
            # --------------------------------------------------
            # |             Start Trial                        |
            # --------------------------------------------------
            while continueRoutine:
                frameN = frameN + 1 # number of completed frames (so 0 is the first frame)
                
                # Stimulus updates
                if frameN >= off2On_isi and stim.status == NOT_STARTED:
                    if self.parallel_port_exists:
                        # callOnFlip(function, *args, **kwargs): Call a function immediately AFTER the next .flip() command.
                        self.win.callOnFlip(self._sendTrigger, triggerSignal) 
                    stim.frameNStart = frameN # exact frame index
                    stim.tStart = self.dataSaveClock.getTime()
                    stim.autoDraw = True
                
                if self.parallel_port_exists and self.port.status == STARTED and self.trialClock.getTime() >= 0:
                    self.port.status = STOPPED
                    self.port.setData(0) # set the trigger back to 0
                
                # check for quit (the Esc key)
                if event.getKeys(keyList=['escape']):
                    core.quit()
                
                if stim.status == STARTED and frameN >= (stim.frameNStart + self.nFrStim):
                    stim.autoDraw = False
                    continueRoutine = False
                
                self.win.flip() # makes all changes visible
            
            self.trialHandler.addData('tPresentation', stim.tStart)
            # indicates to the ExperimentHandler that the current trial has 
            # ended and so further addData() calls correspond to the next trial
            self.thisExp.nextEntry() 
            
            # if you want to stop the runOddball function at some index to collect responses, you can use stopIndex
            if self.trialHandler.thisN == stopIndex:
                break
        
        if waitbeforecontinue > 0:
            # I am not sure but I hope that hogCPUperiod = waitbeforecontinue 
            # will make sure that the last trigger is set back to 0
            core.wait(waitbeforecontinue) # if you don't wait here, the 
            # presentation of the last stimulus will be directly followed by 
            # the next routine => in the case of msvr, win will be instantly closed down
        
        if self.trackFrIntervals: self.win.recordFrameIntervals = False
    
    def inputCount(self):
        answer = self.textInput.intInputRoutine(
            'Wieviele Stimuli der vorgegebenen Form haben Sie gezählt? '\
            'Bestätigen Sie Ihre Eingabe mit Enter.')
        self.thisExp.addData('subj_count_oddb', answer)
    
    def getIsiFrList(self): 
        return self.isi_list
    
    def saveFrIntervals(self, filename = None, clear = False):
        if not self.trackFrIntervals:
            logging.error('You have to set trackFrIntervals to True, '\
                          'otherwise there is nothing to save.')
        self.win.saveFrameIntervals(filename, clear)
    
    def instruction(self, captureScreenshot = False):
        self.mouse.setVisible(False) # hide the mouse
        self.deviant.pos=(-100, -100) # in pixel
        self.standard.pos=(100, -100) # in pixel
        if event.getKeys(['escape']):
            core.quit()
        event.clearEvents()
        for i in [self.instructionTxt, self.deviant, self.standard]:
            i.draw()
        self.win.flip()
        
        if captureScreenshot: self.win.getMovieFrame()
        
        continueRoutine = True
        while continueRoutine:
            # check for quit (the Esc key) and space
            if event.getKeys(['escape']):
                core.quit()
            elif event.getKeys(['space']):
                continueRoutine = False
    
    def reminder(self):
        self.mouse.setVisible(False) # hide the mouse
        self.deviant.pos=(0, 0) # in pixel
        if event.getKeys(['escape']):
            core.quit()
        event.clearEvents()
        self.instructionTxt.text = 'Zur Erinnerung sehen Sie unten noch '\
            'einmal die Form, die Sie zählen müssen. '\
            'Mit der Leertaste beginnen Sie die zweite Hälfte.'
        for i in [self.instructionTxt, self.deviant]:
            i.draw()
        self.win.flip()
        continueRoutine = True
        while continueRoutine:
            # check for quit (the Esc key) and space
            if event.getKeys(['escape']):
                core.quit()
            elif event.getKeys(['space']):
                continueRoutine = False
    
    def _sendTrigger(self, signal): # can only be called from within the class
        self.port.status = STARTED
        self.port.setData(signal)
        self.trialClock.reset()
        self.trialClock.add(self.triggerlen)
    
    def _stimsList(self, ntrials, pdeviants, maxNConsecStan):
        #        
        # draw indices for deviants: trials are grouped into pairs; within
        #   these pairs, the first is always a standard to avoid that multiple 
        #   deviants following each other (0 is deviant, 1 is standard)
        assert ntrials%2 == 0, 'The number of deviants should be divisible by 2'
        assert (ntrials*pdeviants).is_integer(), "ntrials*pdeviants must "\
            "return an integer (this warning could be missleading because of "\
            "python's imprecise representation)"
        
        # there are (ntrials/2)*(pdeviants*2) pairs with standards and deviants (1, 0) 
        # and ntrials/2*(1-(pdeviants*2)) pairs w/o a deviant (1, 1)
        pairsStims = int(ntrials*pdeviants)*[(1, 0)] + int((ntrials/2)*(1-(pdeviants*2)))*[(1, 1)]
        
        h =0
        while True:
            h +=1
            np.random.shuffle(pairsStims) # returns None; shuffles the original list
            indecesPairs = [-1]+[i for i, e in enumerate(pairsStims) if e == (1,0)]+[len(pairsStims)] # the list of indeces plus its ends -1 and len(pairsStims) = 150
            diffPairsIndeces = [t - s for s, t in zip(indecesPairs, indecesPairs[1:])]
            if max(diffPairsIndeces) <= int((maxNConsecStan)/2):
                break
            elif h > 50:
                print('Had to re-shuffle too often.')
                core.quit()
        logging.warn('Shuffling List %s times' %(h))
        
        stims=[]
        for i in pairsStims:
            for j in i:
                stims.append(j)
        logging.exp('n deviants in the stims list for Oddball: ' + str(stims.count(0)))
        
        return stims
    
    def _isiList(self, nfr_on2onisi_lower, nfr_on2onisi_upper, nFrStim, ntrials):
        
        # draw ntrials random integers from the “discrete uniform” distribution of the specified dtype in the “half-open” interval [low, high). 
        assert nfr_on2onisi_lower > nFrStim, 'The minimum onset to onset isi must be longer than the presentation of a stimulus.'
        framesIsi_list = np.random.randint(nfr_on2onisi_lower, nfr_on2onisi_upper+1, size = ntrials) 
        logging.exp('Mean value of the isi_list in Oddball: ' + str(np.mean(framesIsi_list)))
        
        return framesIsi_list
    
    def drawStimForScreenshot(self):
        # centre the stimuli in the middle
        self.deviant.pos = self.standard.pos = (0,0)
        
        # screenshot deviant
        self.deviant.draw()
        self.win.flip()
        self.win.getMovieFrame()
        
        # screenshot standard
        self.standard.draw()
        self.win.flip()
        self.win.getMovieFrame()
        
        # screenshot empty
        self.win.flip()
        self.win.getMovieFrame()
        
        self.saveScreenshot(fn = 'testdata/stimuli.png')
        
    
    def saveScreenshot(self, fn = 'testdata/oddballScreenshot.png'):
        self.win.saveMovieFrames(fn, 
                                 codec='libx264', 
                                 fps=30, 
                                 clearFrames=True)
    
    
    def saveTrialList(self, fn = 'testdata/oddballTrialList.csv'):
        trialList = self.trialHandler.trialList
        keys = trialList[0].keys()
        with open(fn, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(trialList)
    


