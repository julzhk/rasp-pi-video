import time
import threading

class timer_control(threading.Thread):
    def run(self):
        threading._sleep(self.sleeptime)
        print "Do this once after %s seconds, then quit", self.sleeptime
        if self.funktion:
            self.funktion(*self.args)
        exit()

    def __init__(self,funktion=None, args = None, sleeptime=4):
        self.funktion = funktion
        self.args = args
        self.sleeptime = sleeptime
        threading.Thread.__init__(self)

# t = timer_control(funktion=do_once)
# t.start()
# while True:
#     print 'threads', threading.active_count(),
#     time.sleep(1)
#     print '.',

