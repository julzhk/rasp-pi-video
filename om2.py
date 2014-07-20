import threading
import pygame
import re
from threading import Thread, Timer
from time import sleep
from pprint import pprint
import time
from threading import Timer
import pexpect

import pexpect
import time

pygame.init()
pygame.mixer.quit()
pygame.display.init()
pygame.mouse.set_visible(False)
wincolor = 130, 30, 30
fg = 250, 240, 230
bg = 5, 5, 5
# fill background
font = pygame.font.Font(None, 30)
msg = 'boo1'
size = font.size(msg)
ren = font.render(msg, 1, fg)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.fill(wincolor)
screen.blit(ren, (30 + size[0], 40 + size[1]))
pygame.display.update()

sleep(2)

child = pexpect.spawn('/usr/bin/omxplayer -s testc.mov')
time.sleep(6)

killer = pexpect.spawn('pgrep omxplayer')
pslist = killer.read()
print pslist
for pid in pslist.split():
    print pid
    pidkill = 'sudo kill -9 %s' % pid
    print pidkill
    killer = pexpect.spawn('sudo kill -9 %s' % pid)
    print killer.read()
    print '-' * 8

wincolor = 130, 30, 30
fg = 21, 240, 230
bg = 5, 5, 5
# fill background
font = pygame.font.Font(None, 30)
msg = 'boo2'
size = font.size(msg)
ren = font.render(msg, 1, fg)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.fill(wincolor)
screen.blit(ren, (30 + size[0], 40 + size[1]))
pygame.display.update()

sleep(2)
