#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

@author: LKirst

Psychpy v2020.1.3
Python 3.6

"""

from builtins import object

from matplotlib import pyplot as plt
import numpy as np

from psychopy import logging, core

class ParallelPort(object):
    
    def __init__(self, address, showplot = False):
        """This is a constructor to simulate a parallel port. Normally, this method would 
        set the memory address of your parallel port,
        to be used in subsequent calls to this object
        
        Common port addresses:
        
            LPT1 = 0x0378 or 0x03BC
            LPT2 = 0x0278 or 0x0378
            LPT3 = 0x0278
        """
        logging.critical("A parallel port is being simulated. No actual triggers are sent!")
        
        self.status = None
        self.showplot = showplot
        self.pinsstate_current  = np.zeros(  (8, 1),          dtype = np.uint8)
        
        ### track the parallel port status biosemi style in a plot
        
        if self.showplot:
            
            self.timeinterval   = 10 # in seconds
            self.datapoints     = 600 # how many data points will be in the timeinterval
            self.timeperpoint   = self.timeinterval/self.datapoints # how much time per point in interval
            self.lastindex      = 0
            
            # np.uint8 is an unigned integer and allows unpacking into binary-valued output arrays => the state of my pins
            self.pinsstate_interval = np.random.randint(0,2, (8, self.datapoints), dtype=np.uint8)
                
            self.fig = plt.figure()
            self.ax  = self.fig.add_subplot(111)
            
            self.fig.canvas.draw()   # note that the first draw comes before setting data
            
            self.pinplot = self.ax.imshow(self.pinsstate_interval, aspect = 'auto', interpolation="None", cmap=plt.cm.gray)
            
            self.timer = core.Clock()
    
    def setData(self, data):
        """Set the data to be presented on the parallel port (one ubyte).
        Alternatively you can set the value of each pin (data pins are
        pins 2-9 inclusive) using :func:`~psychopy.parallel.setPin`
        
        Examples::
        
            parallel.setData(0)  # sets all pins low
            parallel.setData(255)  # sets all pins high
            parallel.setData(2)  # sets just pin 3 high (pin2 = bit0)
            parallel.setData(3)  # sets just pins 2 and 3 high
        
        You can also convert base 2 to int easily in python::
        
            parallel.setData( int("00000011", 2) )  # pins 2 and 3 high
            parallel.setData( int("00000101", 2) )  # pins 2 and 4 high
        """
        
        logging.data('parallel port set to %d' %data)
        
        self._updateState(data = data)
        if self.showplot: self.updateFig()
    
    def setPin(self, pinNumber, state):
        """Set a desired pin to be high(1) or low(0).
        
        Only pins 2-9 (incl) are normally used for data output::
        
            parallel.setPin(3, 1)  # sets pin 3 high
            parallel.setPin(3, 0)  # sets pin 3 low
        """
        
        logging.data('parallel port pin %d set to %d' %(pinNumber, state))
        
        self._updateState(pinNumber = pinNumber, state = state)
        if self.showplot: self.updateFig()
    
    def readData(self):
        """Return the value currently set on the data pins (2-9)
        """
        raise NotImplementedError("I haven't implemented this method for simulation yet.")
    
    def readPin(self, pinNumber):
        """Determine whether a desired (input) pin is high(1) or low(0).

        Pins 2-13 and 15 are currently read here
        """
        return self.pinsstate_current[pinNumber-2,0]
    
    def updateFig(self):
        """
        'Blitting' is a old technique in computer graphics. 
        The general gist is to take an existing bit map (in our case a mostly rasterized figure) and 
        then 'blit' one more artist on top. Thus, by managing a saved 'clean' bitmap, we can only 
        re-draw the few artists that are changing at each frame and possibly save significant amounts of time. 
        """
        
        self.pinplot.set_data(self.pinsstate_interval)
        
        self.ax.draw_artist(self.pinplot) # redraw just the points (not the axis ticks, labels, etc)
        
        self.fig.canvas.blit(self.ax.bbox) # fill in the axes rectangle
        
        plt.pause(0.000001)
        #plt.pause calls canvas.draw(), as can be read here:
        #http://bastibe.de/2013-05-30-speeding-up-matplotlib.html
        #however with Qt4 (and TkAgg??) this is needed. It seems,using a different backend, 
        #one can avoid plt.pause() and gain even more speed.
    
    def _updateState(self, data = None, pinNumber = None, state = None):
        
        if self.showplot:
            
            t = self.timer.getTime()
            if t >= 0:
                self.timer.reset()
                self.timer.add(self.timeinterval)
                t = - self.timeinterval
                
                self.pinsstate_interval.fill(0)
            
            index           = (self.timeinterval+t)//self.timeperpoint # remember: t is negative!
            updateinterval  = np.arange(self.lastindex, index, dtype=np.uint8)
            lenupdint       = len(updateinterval)
            
            # self.pinsstate_current hasn't been updated yet! This is just writing to the array what has happened so far.
            self.pinsstate_interval[:, updateinterval] = np.repeat(self.pinsstate_current, lenupdint, axis = 1) 
            
            self.lastindex = index
        
        if data is not None:
            self.pinsstate_current = np.unpackbits( # unpackbits turns an integer into an array its base two representation
                                                np.array([data], dtype=np.uint8)
                                       ).reshape((8, 1)) # we have to reshape to insert the values in pinsstate_interval
        elif pinNumber is not None:
            self.pinsstate_current[pinNumber-2, 0] = state
        
        

