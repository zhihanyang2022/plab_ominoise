class TimerFactory:

    def __init__(self, win, keyboard):
        self.win, self.keyboard, = win, keyboard
        self.accum = []

    def get_new_timer(self):
        return Timer(win=self.win, keyboard=self.keyboard, accum=self.accum)

class Timer:

    def __init__(self, win, keyboard, accum):
        self.win = win
        self.keyboard = keyboard
        self.accum = accum
        self.times = {
            'start_time':None,
            'end_time':None
        }
        self.start_now = True

    def record_start_time(self):
            self.win.timeOnFlip(self.times, 'start_time')

    def record_end_time(self):
            self.win.timeOnFlip(self.times, 'end_time')

    @property
    def end_now(self):
        self.start_now = False
        return self.keyboard.getKeys(keyList=['space'])

    @property
    def quit_now(self):
        self.start_now = False
        return self.keyboard.getKeys(keyList=['escape'])

    def run_start_procedure(self, start_func):
        self.record_start_time()
        start_func()
        self.win.flip()
        self.start_now = False

    def run_end_procedure(self, end_func):
        self.record_end_time()
        end_func()
        self.win.flip()
        self.accum.append(self)
