import threading
import logging
SLEEPTIME=3

class TimerControl(threading.Thread):
    """
    Use threads to run a function once,after a certain delay.
    """
    def run(self):
        """
            RUN is a magic name in the Threading Library
        """
        threading._sleep(self.sleeptime)
        self.funktion( *self.args)
        exit()

    def __init__(self, funktion=None, args=None):
        self.funktion = funktion
        self.args = args
        self.sleeptime = SLEEPTIME
        threading.Thread.__init__(self)


