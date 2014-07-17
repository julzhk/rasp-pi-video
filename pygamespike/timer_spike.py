import time
import threading
#timer heartbeat in seconds
TIMER_INTERVAL = 4

def do_once():
    print 'done!'

class timer_control(threading.Thread):
    def run(self):
        threading._sleep(4)
        print "Do this once after 4 seconds, then quit"
        if self.funktion:
            self.funktion()
        exit()

    def __init__(self,funktion=None  ):
        self.funktion = funktion
        threading.Thread.__init__(self)

t = timer_control(funktion=do_once)
t.start()
while True:
    print 'threads', threading.active_count(),
    time.sleep(1)
    print '.',