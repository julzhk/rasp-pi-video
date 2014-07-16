import time
import pygame

try:
    import pifacedigitalio
    pfd = pifacedigitalio.PiFaceDigital()
    pfd_installed = True
except ImportError:
    pfd_installed = False

import threading
from threaded_timer import TimerControl

HIDE_MOUSE = True
RESETPIN = 0
GLOVETESTPIN = 1
OFFPIN = 2
STARTPIN = 3
FULLSCREEN = False
FPS = 60
DEBUG = True
MOVIE_FILE='parkinsons.mpg'

def led_off(pin):
    # Wrappers for turn on/off LED by number
    pfd.leds[pin].turn_off()

def turn_off_all_leds():
    [pfd.leds[i].turn_off() for i in range(0, 4)]

def led_on(pin):
    # Wrappers for turn on/off LED by number
    pfd.leds[pin].turn_on()
    # auto off LED in a few seconds
    TimerControl(funktion=led_off,args=[pin]).start()

def activate_glove():
    # turn on LED & turn on both Relays
    led_on(GLOVETESTPIN)
    pfd.relays[0].turn_on()
    pfd.relays[1].turn_on()        

def glovetest():
    # called by button on pin GLOVETESTPIN
    activate_glove()

def off():
    # quit with an exception
    raise

def start():
    global movie
    movie.play()
    led_on(STARTPIN)

def reset():
    global movie,screen
    led_on(RESETPIN)
    movie.rewind()
    blit_screen()
    screen.fill((0,0,0))
    movie.pause()

def debug():
    if pfd_installed:
        for i in range(0, 8):
            print i, ' ', pfd.input_pins[i].value,
        print



def blit_screen():
    global screen,movie_screen
    time.sleep(.01)
    screen.blit(movie_screen, (0, 0))
    pygame.display.update()


def start_project():
    while True:
        try:
            blit_screen()
            clock.tick(FPS)
            print DEBUG & movie.get_frame()
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
            turn_off_all_leds()
            exit()


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.init()
    movie_screen = pygame.Surface((600, 500))
    movie = pygame.movie.Movie(MOVIE_FILE)
    movie.set_display(movie_screen)
    pygame.mouse.set_visible(not HIDE_MOUSE)
    if FULLSCREEN:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((250,500), pygame.RESIZABLE)
    print screen
    print movie.get_size()

    start_project()
