import time
import sys
import pygame
import pexpect
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN
import logging_data
import logging_decorator
import random
import threading
from threading import Timer
import logging


try:
    import pifacedigitalio

    pfd = pifacedigitalio.PiFaceDigital()
    pfd_installed = True
except ImportError:
    pfd_installed = False

pfd.relays[0].turn_on()
pfd.relays[1].turn_on()

time.sleep(3)
pfd.relays[1].turn_off()
pfd.relays[0].turn_off()
