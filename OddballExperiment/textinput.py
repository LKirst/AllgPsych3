"""

@author: LKirst

Psychpy v3.0
Python 3.6

"""

import re
from psychopy import visual, event, core, logging

class TextInput:
    
    def __init__(self, win):
        self.question       = visual.TextStim(
            win, anchorHoriz='left', units = 'norm', height = .08, 
            pos = (-.5, .5), name = 'question', autoLog = False)
        self.displayInput   = visual.TextStim(
            win, anchorHoriz='left', units = 'norm', height = .08, 
            pos = (-.5, -.1), name = 'inputText', autoLog = False)
        self.win = win
    
    def intInputRoutine(self, questionText):
        
        theseKeys = ''
        inputText = ''
        
        if event.getKeys(['escape']):
            core.quit()
        event.clearEvents() # delete all responses in the buffer
        
        self.question.autoDraw = True
        self.displayInput.autoDraw = True
        
        continueRoutine = True
        while continueRoutine:
            
            theseKeys = event.getKeys()
            n = len(theseKeys)
            i = 0
            
            while i < n:
                if theseKeys[i] == 'escape':
                    core.quit()
                elif theseKeys[i] == 'return':
                    if len(inputText)>0: # only allow return once something has been entered
                        # pressing RETURN means time to stop
                        continueRoutine = False
                        break
                    else:
                        i += 1
                elif theseKeys[i] == 'backspace':
                    inputText = inputText[:-1]  # lose the final character
                    i = i + 1
                elif re.match(r"num_[0-9]", theseKeys[i]):
                    # the number pad on the key board has the keys 'num_0' to 'num_9'
                    inputText += theseKeys[i][-1]
                    i += 1
                else:
                    if len(theseKeys[i]) == 1 and theseKeys[i].isdigit():
                        inputText += theseKeys[i]
                    i += 1
            
            self.question.text      = questionText
            self.displayInput.text  = inputText
            
            self.win.flip()
        
        self.question.autoDraw = False
        self.displayInput.autoDraw = False
        
        inputInt = int(inputText)
        logging.data(inputInt)
        return inputInt
    
    def textInputRoutine(self, questionText):
        
        theseKeys = ''
        inputText = ''
        shift_flag = False
        
        if event.getKeys(['escape']):
            core.quit()
        event.clearEvents() # delete all responses in the buffer
        
        self.question.autoDraw = True
        self.displayInput.autoDraw = True
        
        continueRoutine = True
        while continueRoutine:
            
            theseKeys = event.getKeys()
            n = len(theseKeys)
            i = 0
            
            while i < n:
                if theseKeys[i] == 'escape':
                    core.quit()
                elif theseKeys[i] == 'return':
                    if len(inputText)>0: # return only has an effect if something has been entered
                        continueRoutine = False
                        break
                    else:
                        i += 1
                elif theseKeys[i] == 'backspace':
                    inputText = inputText[:-1]  # delete the last input
                    i += 1
                elif theseKeys[i] == 'space':
                    inputText += ' '
                    i += 1
                elif theseKeys[i] in ['lshift', 'rshift']:
                    shift_flag = True
                    i += 1
                else:
                    if len(theseKeys[i]) == 1: # ctrl or other multi-letter keys are ignored
                        if shift_flag:
                            inputText += chr( ord(theseKeys[i]) - ord(' '))
                            shift_flag = False
                        else:
                            inputText += theseKeys[i]
                    i += 1
            
            self.question.text      = questionText
            self.displayInput.text  = inputText
            self.win.flip()
        
        self.question.autoDraw = False
        self.displayInput.autoDraw = False
        
        logging.data(inputText)
        return inputText