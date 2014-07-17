__author__ = 'julz'
from threaded_timer import TimerControl

def printer(n=44):
    print n


TimerControl(funktion=printer,args=[991]).start()
