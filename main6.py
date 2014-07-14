__author__ = 'julz'
import threading
import time
from time import sleep
import pifacedigitalio

import pygame

from threaded_timer import timer_control

pfd = pifacedigitalio.PiFaceDigital()

HIDE_MOUSE = True
RESETPIN = 0
GLOVETESTPIN = 1
OFFPIN = 2
STARTPIN = 3
FPS = 60
DEBUG = True
MOVIE_FILE = 'parkinsons.mpg'


def led_off(pin):
    pfd.leds[pin].turn_off()


def led_on(pin):
    pfd.leds[pin].turn_on()


def activate_glove():
    led_on(GLOVETESTPIN)
    timer_control(funktion=led_off, args=[GLOVETESTPIN]).start()
    pfd.relays[0].turn_on()
    pfd.relays[1].turn_on()


def glovetest():
    activate_glove()


def off():
    raise


def start():
    global movie
    movie.play()
    led_on(STARTPIN)
    timer_control(funktion=led_off, args=[STARTPIN]).start()


def reset():
    global movie, screen
    led_on(RESETPIN)
    timer_control(funktion=led_off, args=[RESETPIN]).start()
    movie.rewind()
    blit_screen()
    screen.fill((0, 0, 0))
    movie.pause()


def debug():
    for i in range(0, 8):
        print i, ' ', pfd.input_pins[i].value,
    print


def turn_off_leds():
    [pfd.leds[i].turn_off() for i in range(0, 4)]


def blit_screen():
    global screen, movie_screen
    time.sleep(.01)
    screen.blit(movie_screen, (0, 0))
    pygame.display.update()


class PhaseChange(Exception):
    pass


class do_screensaver(PhaseChange):
    pass


class do_instructions(PhaseChange):
    pass


class do_mainmovie(PhaseChange):
    pass


class do_replaceheadphones(PhaseChange):
    pass


class do_quit(PhaseChange):
    pass


def screensaver():
    print 'screensaver'
    sleep(1)
    raise


def instructions():
    print 'instructions'
    sleep(3)
    raise


def mainmovie():
    print 'movie'
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
            turn_off_leds()
            exit()


def replaceheadphones():
    print 'reset'
    raise


def quit():
    exit()


def main():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.init()
    movie_screen = pygame.Surface((600, 500))
    movie = pygame.movie.Movie(MOVIE_FILE)
    movie.set_display(movie_screen)
    pygame.mouse.set_visible(not HIDE_MOUSE)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    print screen
    print movie.get_size()

    run_phase = screensaver
    while True:
        try:
            run_phase()
        except do_screensaver:
            run_phase = screensaver
        except do_instructions:
            run_phase = instructions
        except do_mainmovie:
            run_phase = mainmovie
        except do_replaceheadphones:
            run_phase = replaceheadphones
        except do_quit:
            run_phase=quit

if __name__ == "__main__":
    main()
