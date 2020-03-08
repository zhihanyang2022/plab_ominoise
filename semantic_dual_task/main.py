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

# ========== BEGIN WINDOW =========

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

# ========= END WINDOW =========

# ========== BEGIN COMPONENTS ==========

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

instructionsClock = core.Clock()
instructions_text = visual.TextStim(win=win, name='instructions_text',
    text='Welcome!',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    languageStyle='LTR',
    depth=0.0);
instructions_keyresp = keyboard.Keyboard()

show_word_clock = core.Clock()
show_word = visual.TextStim(win=win, name='show_word',
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

# constants

kNUM_CONDS = 4
kNUM_WORDS_PER_COND = 75

# prepare word lists

noise_conds = np.array(['quiet', 'info_noise', 'ener_noise', 'modu_ener_noise'])
np.random.shuffle(noise_conds)

with open('sdt_vocab.txt', 'w+') as txt_f:
    for word in sdt_words:
        txt_f.write(word + '\n')

def get_word_lists(sdt_vocab_fpath):
    with open(sdt_vocab_fpath, 'r') as txt_f:
        words = [word.rstrip() for word in txt_f.readlines()]
    np.random.shuffle(words)
    return np.split(np.array(words), kNUM_CONDS)

word_lists = get_word_lists('sdt_vocab.txt')

def get_interstim_intervals_for_all(size=300):
    choices = np.arange(2500, 3500 + 1, 250)
    return np.random.choice(choices, size=size)

interstim_intervals = get_interstim_intervals_for_all()

# loops

word_countdown = core.CountdownTimer()

timer_factory2 = TimerFactory(win=win, keyboard=defaultKeyboard)

for i, noise in enumerate(noise_conds):

    word_list = word_lists[i]

    for j, word in enumerate(word_list):

        show_word.setText(word)
        interstim_interval = interstim_intervals[i * kNUM_WORDS_PER_COND + j]

        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        show_word_clock.reset(-_timeToFirstFrame)

        word_countdown.reset(interstim_interval)
        while word_countdown.getTime() > 0:

            tThisFlip = win.getFutureFlipTime(clock=show_word_clock)

            if tThisFlip >= 0.0-frameTolerance:
                show_word.setAutoDraw(True)
                win.flip()

            if defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()

    # LASTTIME:

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
