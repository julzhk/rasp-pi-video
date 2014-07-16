import threading
import logging

class TimerControl(threading.Thread):
    """
    Use threads to run a function once,after a certain delay.
    """
    def run(self):
        """
            RUN is a magic name in the Threading Library
        """
        threading._sleep(self.sleeptime)
        try:
            logging.INFO("Timer wait: %s seconds, then %s" % (self.sleeptime, self.funktion.__name__))
        except TypeError:
            logging.INFO("Do this once after %s seconds, then?? %s" % (self.sleeptime, self.funktion))
        if self.funktion:
            self.funktion(*self.args)
        exit()

    def __init__(self, funktion=None, args=None, sleeptime=3):
        self.funktion = funktion
        self.args = args
        self.sleeptime = sleeptime
        threading.Thread.__init__(self)


