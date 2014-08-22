import threading
import pygame
import re
from threading import Thread, Timer
from time import sleep
from pprint import pprint
import time
from threading import Timer
import pexpect


class OmxControl(threading.Thread):
    """
    Use threads to run a function once,after a certain delay.
    """
    def run(self, mediafile):
        """
            RUN is a magic name in the Threading Library
        """
        args = ''
        _LAUNCH_CMD = '/usr/bin/omxplayer -s %s %s'
        cmd = _LAUNCH_CMD % (mediafile, args)
        self._process = pexpect.spawn(cmd)
        self.pid = self._process.pid
        # need to let the video initialize
        sleep(0.1)


pygame.init()
pygame.mixer.quit()
pygame.display.init()
pygame.mouse.set_visible(False)
wincolor = 130, 30, 30
fg = 250, 240, 230
bg = 5, 5, 5
# fill background
font = pygame.font.Font(None, 30)
msg = 'boo'
size = font.size(msg)
ren = font.render(msg, 1, fg)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.fill(wincolor)
screen.blit(ren, (30 + size[0],40 + size[1]))
pygame.display.update()

sleep(2)

def omxplayer(fn):
    _LAUNCH_CMD = '/usr/bin/omxplayer -s %s %s'
    cmd = _LAUNCH_CMD % (fn, '')
    _process = pexpect.spawn(cmd)
    return _process.pid

t1 = threading.Thread(target=omxplayer, args=('testb.mp4',))
t1.start()
