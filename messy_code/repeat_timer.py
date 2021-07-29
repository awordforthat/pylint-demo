'''
A basic interval timer.
'''

from threading import Timer

class RepeatedTimer():
    '''
    A basic interval timer.
    '''
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        '''
        Starts the timer.
        '''
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        '''
        Creates a new timer and starts it (if not already running).
        '''
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        '''
        Stops the timer
        '''
        self._timer.cancel()
        self.is_running = False
