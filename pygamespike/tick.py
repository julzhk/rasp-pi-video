# Example 17 Multithreading
import threading
class Animate (threading.Thread):
    def run(self):
        for count in range(0, int(self.duration // self.interval)):
            threading._sleep(self.interval)
            print "Tick"
    def __init__(self, interv, durat):
        threading.Thread.__init__(self)
        self.interval = interv
        self.duration = durat
anim = Animate(1.5, 6.0)
anim.start()
