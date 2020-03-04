from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock
from psychopy.hardware import keyboard

# my imports
import os
import sys
import time
import keyboard as k
import json
sys.path.append('../scripts')
from time_util import Timer, TimerFactory

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '3.2.4'
expName = 'demo'  # from the Builder filename that created this script
expInfo = {'participant': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

with open(filename + '.json', 'a') as json_f:
    json.dump(expInfo, json_f)

frameTolerance = 0.001  # how close to onset before 'same' frame

# ========== BEGIN COMPONENTS ==========

# Setup the Window
win = visual.Window(
    size=(1024, 768), fullscr=True, screen=0,
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "instructions"
instructionsClock = core.Clock()
instructions_text = visual.TextStim(win=win, name='instructions_text',
    text='Welcome!',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    languageStyle='LTR',
    depth=0.0);
instructions_keyresp = keyboard.Keyboard()

# Initialize components for Routine "show_condition"
show_conditionClock = core.Clock()
show_condition_text = visual.TextStim(win=win, name='show_condition_text',
    text='default text',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    languageStyle='LTR',
    depth=0.0);

# ========== BEGIN INSTRUCTIONS ==========

_timeToFirstFrame = win.getFutureFlipTime(clock="now")
instructionsClock.reset(-_timeToFirstFrame)

timer_factory = TimerFactory(win=win, keyboard=defaultKeyboard)

timer = timer_factory.get_new_timer()

while not timer.end_now:

    tThisFlip = win.getFutureFlipTime(clock=instructionsClock)

    if tThisFlip >= 0.0-frameTolerance:
        instructions_text.setAutoDraw(True)
        win.flip()

    if defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()

instructions_text.setAutoDraw(False)
win.flip()

# ========== END INSTRUCTIONS ==========

# ========== BEGIN EXP ==========

routineTimer = core.CountdownTimer()

# level 1: loop through the noise conditions
loop_noises = data.TrialHandler(nReps=1, method='random',
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('csvs/noise_conditions.csv'),
    seed=None, name='loop_noises')

timer_factory2 = TimerFactory(win=win, keyboard=defaultKeyboard)

for thisNoise in loop_noises:
    condition = thisNoise['condition']

    # level 2: loop through the set of word lists
    # print(condition)
    loop_lists = data.TrialHandler(nReps=1, method='random',
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('csvs/condition_{}_wlists_indices.csv'.format(condition)),
        seed=None, name='loop_lists')

    for thisList in loop_lists:
        wlist_index = thisList['wlist_index'] # initialize variable "wlist_index"

        # level 3: loop through words
        # print(wlist_index)
        loop_words = data.TrialHandler(nReps=1, method='random',
            extraInfo=expInfo, originPath=-1,
            trialList=data.importConditions('csvs/{}.csv'.format(wlist_index)),
            seed=None, name='loop_words')

        for thisWord in loop_words:
            word = thisWord['word'] # initialize variable "word"

            show_condition_text.setText(word)  # show word on screen

            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            show_conditionClock.reset(-_timeToFirstFrame)

            routineTimer.reset(0.01000)
            while routineTimer.getTime() > 0:

                tThisFlip = win.getFutureFlipTime(clock=show_conditionClock)

                if tThisFlip >= 0.0-frameTolerance:
                    show_condition_text.setAutoDraw(True)
                    win.flip()

                if defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()

        timer = timer_factory2.get_new_timer()

        def start_func():
            show_condition_text.setText("****")
            show_condition_text.setAutoDraw(True)

        def end_func():
            show_condition_text.setAutoDraw(False)

        while True:
            if timer.start_now:
                timer.run_start_procedure(start_func)
            elif timer.end_now:
                timer.run_end_procedure(end_func); break
            elif timer.quit_now:
                core.quit()
            else:
                timer.win.flip()

# ========== END EXP ==========

### save information from used components into a csv file

for i, cmp in enumerate(timer_factory2.accum):
    print('index {} | start: {} | stop: {}'.format(i+1, cmp.times['start_time'], cmp.times['end_time']))

# Flip one final time so any remaining win.callOnFlip()
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

win.close()
core.quit()
