# -*- coding: utf-8 -*-
"""
Created Apr 2020

@author: LKirst

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# # If you want to see the plots in a dedicated matplotlib window
# get_ipython().run_line_magic('matplotlib', 'qt')

# If you want to see the plots in the spyder plot window
get_ipython().run_line_magic('matplotlib', 'inline')

# %% Functions to set the position of electrodes

def setPos(mark4, chan, mirrorChanX = None, mirrorChanY = None, mirrorChanXY = None,
           x = None, y = None, pos = None,
           defaultIndx = None, customIndx = None):
    """
    Add channel position and index to a dataframe.

    Parameters
    ----------
    mark4 : pandas.dataframe
        A dataframe with the channels as indices.
    chan : str
        A channel name, which must be a valid index in mark4.
    mirrorChanX : str, optional
        The index of the row for the channel which is at the same 
        position except for a mirrored x-value, i.e. mirrored allong the 
        y-axis. 
        The default is None.
    mirrorChanY : str, optional
        The index of the row for the channel which is at the same 
        position except for a mirrored y-value, i.e. mirrored allong the 
        x-axis. 
        The default is None.
    x : float, optional
        The default is 0.
    y : float, optional
        The default is 0.
    defaultIndx : int, optional
        The default is None.
    customIndx : int, optional
        The default is None.

    Returns
    -------
    mark4: pandas.dataframe

    """
    if pos is not None:
        if x is not None or y is not None: warnings.warn(
                'You can only use either the pos argument or x and y, not both.')
        x = pos[0]
        y = pos[1]
    else:
        if x is None: x = 0
        if y is None: y = 0

    i = 0
    for channel, xMult, yMult in [(chan, 1, 1), (mirrorChanX, -1, 1), 
                                  (mirrorChanY, 1, -1), (mirrorChanXY, -1, -1)]:
        if channel is not None:
            assert channel in mark4.index, print(channel, 'is not an index of your df.')
        else:
            continue
        
        mark4.loc[channel, 'posx']  = x*xMult
        mark4.loc[channel, 'posy']     = y*yMult
        if defaultIndx and len(defaultIndx) > i:
            mark4.loc[channel, 'defaultIndx'] = defaultIndx[i]
        if customIndx and len(customIndx) > i: 
            mark4.loc[channel, 'customIndx']  = customIndx[i]
        i += 1
            
    return(mark4)

def getPos(mark4, chan):
    return( ( mark4.loc[chan, 'posx'], mark4.loc[chan, 'posy'] ) )


def pOnCirc(radius, percent):
    """
    

    Parameters
    ----------
    radius : float
        The radius of the circle, on which your point lies.
    percent : float
        The distance of the point you seek from the point (0, radius).
        Distance must be given in percentage.

    Returns
    -------
    point : ( x, y )

    """
    x = radius*np.sin(np.deg2rad(360*percent/100))
    y = radius*np.cos(np.deg2rad(360*percent/100))
    return( (x, y) )




def pOnCircHalf(a, c, e):
    
    # There are three points on a circle: a, c, and e
    # We are interested in point b, which is in the middle between a and c 
    # on the circumference
    # For that we need: 
    #   point n, which halves the line between a and c
    #   point v, which halves the line between c and e
    #   point m, the centre of the circle
    
    # a point on the line that is orthagonal to a2c and a vector of its direction
    # (i.e. the line is defined)
    n          = 0.5 * np.add(a, c)
    ac_v       = np.subtract(c, a)
    ac_vnorm   = findNormal(ac_v)
    
    # a points on the line that is orthagonal to c2e  and a vector of its direction
    # (i.e. the line is defined)
    v           = 0.5 * np.add(c, e)
    ce_v        = np.subtract(e, c)
    ce_vnorm    = findNormal(ce_v)
    
    # the centre of the circle defined by a, c, e is the intersection 
    # of the two lines defined above
    m = seg_intersect(n, n+ac_vnorm, v, v+ce_vnorm)
    
    # the radius of the circle
    r = abs(np.linalg.norm(np.subtract(a, m)))
    
    mn_v = n-m    
    pb = m + (mn_v * r / np.linalg.norm(mn_v))
    
    return(pb)



def seg_intersect(a1,a2, b1,b2) :
    """
    Find intersection of:
    the line defined by points a1, a2 and
    the line defined by points b1, b2
    """
    a1a2_v = a2-a1
    b1b2_v = b2-b1
    b1a1_v = a1-b1
    a1a2_vnorm = findNormal(a1a2_v)
    
    denom = np.dot( a1a2_vnorm, b1b2_v)
    num = np.dot( a1a2_vnorm, b1a1_v )
    
    return (num / denom)*b1b2_v + b1


def findNormal( a ) :
    """
    

    Parameters
    ----------
    a : array_like
        A two-dimensional array.

    Returns
    -------
    b : ndarray
        Array perpendicular to a.

    """
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return(b)

# %% Functions to plot and store the head model

def plotHead(mark4, limits = [-.6, .6], title = None, axisOff = False):
    
    fig, ax = plt.subplots(figsize = (8, 8))
    
    r = np.linalg.norm(getPos(mark4, 'Fp1')) # radius of the circle
    circle = plt.Circle((0,0), 
                        r, 
                        fill = False)
    ax.add_artist(circle)
    
    mark4Complete = mark4[['posx', 'posy']].dropna()

    for lbl in mark4Complete.index:
        plt.annotate(lbl,
                     (mark4Complete.loc[lbl, 'posx'], mark4Complete.loc[lbl, 'posy']),
                     textcoords = 'offset pixels', xytext = (0, 5))
        # 'bo-' means blue color, round points
        plt.plot(mark4Complete['posx'], mark4Complete['posy'], 'bo')
    
    plt.axis('scaled')
    ax.set_xlim(limits)
    ax.set_ylim(limits)
    ax.invert_yaxis()
    
    plt.plot(0, -(r + 0.1*r), marker = "^", markersize = 15) # plot the nose
    
    if axisOff: plt.axis('off')
    else: sns.despine() # get rid of the bounding box
    
    if title is not None: plt.title(title) # add a title
    
    plt.show()
    return(ax)


def writeNewPosFile(mark4, file = 'electrode_positions_default_KU.txt'):
    mark4Complete = mark4.loc[:, ['posx', 'posy', 'customIndx']].dropna()
    mark4Complete = mark4Complete.sort_values(by = 'customIndx')
    # I don't know why, but this last line with the coordinates of Cz seems to be required
    mark4Complete = mark4Complete.append(
        pd.Series({'posx':0, 'posy':0}), 
        ignore_index = True) 
    mark4Complete.iloc[:,[0,1]].to_csv(file, index = False, header = ['x', 'y'])


# %% Electrodes in the 10-10 system

# Some channels are known under different names: (we use the option on the right side)
#   T3 = T7
#   T4 = T8
#   T5 = P7
#   T6 = P8
channels = ['Nz', 'Iz',
            'Fpz', 'Fp1', 'Fp2', 
            'AFz', 'AF3', 'AF4', 'AF7', 'AF8',
            'Fz', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 
            'FCz', 'FC1', 'FC2', 'FC3', 'FC4', 'FC5', 'FC6', 'FT7', 'FT8',
            'Cz', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'T7', 'T8', 'T9', 'T10',
            'CPz','CP1', 'CP2', 'CP3', 'CP4', 'CP5', 'CP6', 'TP7', 'TP8',
            'Pz', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 
            'POz', 'PO3', 'PO4', 'PO7', 'PO8',
            'Oz', 'O1', 'O2']

mark4 = pd.DataFrame(np.nan, 
                     index = channels, 
                     columns = ['posx', 'posy', 'defaultIndx', 'customIndx'])

# %% Set values based on the default file, used by the OpenBCI GUI (v4.2.0)

# File location: ~\OpenBCI_GUI\data\electrode_positions_default.txt

mark4 = setPos(mark4, 'Cz', x = 0, y = 0, customIndx = [8]) # The center of the head circle
mark4 = setPos(mark4, 'Fp1', 'Fp2',   pos = (-.125, -.416), defaultIndx = [1, 2])
mark4 = setPos(mark4, 'C3', 'C4',     pos = (-.2, 0),       defaultIndx = [3, 4])
mark4 = setPos(mark4, 'P7', 'P8',     pos = (-.3425, .27),  defaultIndx = [5, 6])
mark4 = setPos(mark4, 'O1', 'O2',     pos = (-.125, .416),  defaultIndx = [7, 8])
mark4 = setPos(mark4, 'F7', 'F8',     pos = (-.3425,-.27),  defaultIndx = [9, 10])
mark4 = setPos(mark4, 'F3', 'F4',     pos = (-.18,  -.15),  defaultIndx = [11, 12])
mark4 = setPos(mark4, 'T7', 'T8',     pos = (-.416, 0),     defaultIndx = [13, 14])
mark4 = setPos(mark4, 'P3', 'P4',     pos = (-.18, .15),    defaultIndx = [15, 16])

plotHead(mark4, title = 'OpenBCI Mark IV Default')


# %% Custom setup

# The placement of the electrodes is based on:
# Jurcak, V., Tsuzuki, D., & Dan, I. (2007). 10/20, 10/10, and 10/5 systems revisited: Their validity as relative head-surface-based positioning systems. NeuroImage, 34(4), 1600–1611. https://doi.org/10.1016/j.neuroimage.2006.09.024

customIndeces = [
    ('Fp1', 1), # electrodes 1-8 are connected to the Cyton board
    ('Fp2', 2),
    ('F3',  3),
    ('Fz',  4),
    ('F4',  5),
    ('FC2', 6),
    ('C3',  7),
    ('Cz',  8),
    ('C4',  9), # electrodes 9-16 are connected to the Daisy board
    ('P7', 10),
    ('P3', 11),
    ('Pz', 12),
    ('P4', 13),
    ('P8', 14),
    ('O1', 15),
    ('O2', 16)
    ]

for chan, indx in customIndeces:
    assert chan in mark4.index
    mark4.loc[chan, 'customIndx'] = indx

# len(Nz to Iz) = len(Cz to Nz)*2
#               = (len(Cz to Fp1)*5/4)*2
lenNzToIz = np.sqrt(mark4.loc['Fp1','posx']**2 + mark4.loc['Fp1', 'posy']**2)*1.25*2

# Sagital central reference curve (midline)
mark4 = setPos(mark4, 'FCz', mirrorChanY = 'CPz',   y = -lenNzToIz*0.1)
mark4 = setPos(mark4, 'Fz',  mirrorChanY = 'Pz',    y = -lenNzToIz*0.2)
mark4 = setPos(mark4, 'AFz', mirrorChanY = 'POz',   y = -lenNzToIz*0.3)
mark4 = setPos(mark4, 'Fpz', mirrorChanY = 'Oz',    y = -lenNzToIz*0.4)
mark4 = setPos(mark4, 'Nz',  mirrorChanY = 'Iz',    y = -lenNzToIz*0.5)

# Coronal central reference curve (ear to ear)
# For my head-model, I assume that the circumference is a circle, which goes through
# Fp1, Fpz, F7, T7, P7, O1, Oz and their right hemisphere counterparts,
# I can clearly see, that the sequence T7, C3, Cz, etc is incorrectly positioned, 
# because T7 is not on the circumference
mark4 = setPos(mark4, 'T9', 'T10',  x = -lenNzToIz*0.5)
mark4 = setPos(mark4, 'T7', 'T8',   x = -lenNzToIz*0.4)
mark4 = setPos(mark4, 'C5', 'C6',   x = -lenNzToIz*0.3)
mark4 = setPos(mark4, 'C3', 'C4',   x = -lenNzToIz*0.2)
mark4 = setPos(mark4, 'C1', 'C2',   x = -lenNzToIz*0.1)


# circumference
mark4 = setPos(mark4,  'O2', 'O1', 'Fp2', 'Fp1',   pos = pOnCirc(lenNzToIz*.4, 5))
mark4 = setPos(mark4,  'PO8', 'PO7', 'AF8','AF7',  pos = pOnCirc(lenNzToIz*.4, 10))
mark4 = setPos(mark4,  'P8', 'P7',  'F8', 'F7',    pos = pOnCirc(lenNzToIz*.4, 15))
mark4 = setPos(mark4,  'TP8','TP7', 'FT8', 'FT7',  pos = pOnCirc(lenNzToIz*.4, 20))


# F curve
mark4 = setPos(mark4, 'F3', 'F4', 'P3', 'P4',
               pos = pOnCircHalf(
                   getPos(mark4, 'F7'),
                   getPos(mark4, 'Fz'),
                   getPos(mark4, 'F8')))
mark4 = setPos(mark4, 'F5', 'F6', 'P5', 'P6',
               pos = pOnCircHalf(
                   getPos(mark4, 'F7'),
                   getPos(mark4, 'F3'),
                   getPos(mark4, 'F8')))
mark4 = setPos(mark4, 'F1', 'F2', 'P1', 'P2',
               pos = pOnCircHalf(
                   getPos(mark4, 'F3'),
                   getPos(mark4, 'Fz'),
                   getPos(mark4, 'F8')))

# FC curve
mark4 = setPos(mark4, 'FC3', 'FC4', 'CP3', 'CP4',
                pos = pOnCircHalf(
                    getPos(mark4, 'FT7'),
                    getPos(mark4, 'FCz'),
                    getPos(mark4, 'FT8')))
mark4 = setPos(mark4, 'FC5', 'FC6', 'CP5', 'CP6',
                pos = pOnCircHalf(
                    getPos(mark4, 'FT7'),
                    getPos(mark4, 'FC3'),
                    getPos(mark4, 'FT8')))
mark4 = setPos(mark4, 'FC1', 'FC2', 'CP1', 'CP2',
                pos = pOnCircHalf(
                    getPos(mark4, 'FC3'),
                    getPos(mark4, 'FCz'),
                    getPos(mark4, 'FT8')))

# AF curve
mark4 = setPos(mark4, 'AF3', 'AF4', 'PO3', 'PO4',
               pos = pOnCircHalf(
                   getPos(mark4, 'AF7'),
                   getPos(mark4, 'AFz'),
                   getPos(mark4, 'AF8')
                   ))

plotHead(mark4, title = '10-10 System', axisOff = True)


# %% Write to file

plotHead(mark4.dropna(subset = ['customIndx']), title = 'OpenBCI Mark IV KU')

writeNewPosFile(mark4)












