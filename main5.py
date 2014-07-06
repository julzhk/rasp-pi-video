import time
import pifacedigitalio
import threading
#timer heartbeat in seconds
TIMER_INTERVAL = 1.0
class ledcontrol(threading.Thread):
    def run(self):
        for count in range(0, int(self.duration // self.interval)):
            threading._sleep(self.interval)
            print "Tick"
            led_off(self.pin)


    def __init__(self, pin, durat=5):
        threading.Thread.__init__(self)
        self.pin = pin
        self.interval = TIMER_INTERVAL
        self.duration = durat

class glovecontrol(threading.Thread):
    def run(self):
        for count in range(0, int(self.duration // self.interval)):
            threading._sleep(self.interval)
            print "Tick"

    def __init__(self, pin, durat=5):
        threading.Thread.__init__(self)
        self.interval = TIMER_INTERVAL
        self.duration = durat

pfd = pifacedigitalio.PiFaceDigital()
import pygame

HIDE_MOUSE = True
RESETPIN = 0
GLOVETESTPIN = 1
OFFPIN = 2
STARTPIN = 3
FPS = 60
DEBUG = True
def led_off(pin):
    pfd.leds[pin].turn_off()
def led_on(pin,autooff=30):
    pfd.leds[pin].turn_on()
    ledcontrol(pin=pin, durat= 6.0).start()
def activate_glove():
    pass
    led_on(GLOVETESTPIN)

def glovetest():
    activate_glove()

def off():
    raise
    exit()
def start():
    movie.play()
    playmovie()
    led_on(STARTPIN)
def debug():
    for i in range(0, 8):
        print i, ' ', pfd.input_pins[i].value,
    print
def startproject():
    movie = pygame.movie.Movie('parkinsons.mpg')
    pygame.mouse.set_visible(not HIDE_MOUSE)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    print screen
    pygame.display.init()
    print movie.get_size()
    movie_screen = pygame.Surface((600,500))
    movie.set_display(movie_screen)
    while True:
        try:
            time.sleep(.01)
            screen.blit(movie_screen, (0, 0))
            pygame.display.update()
            clock.tick(FPS)
            frame = movie.get_frame()
            if DEBUG:
                debug()
            if pfd.input_pins[RESETPIN].value:
                reset()
            if pfd.input_pins[GLOVETESTPIN].value:
                glovetest()
            if pfd.input_pins[OFFPIN].value:
                off()
            if pfd.input_pins[STARTPIN].value:
                start()
        except:
            [pfd.leds[i].turn_off() for i in range(0,4)]
            exit()

def reset():
    led_on(RESETPIN)
    start_project()



pygame.init()
clock = pygame.time.Clock()

start_project()




