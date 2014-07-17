import time
import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN
import logging_data
import logging_decorator
import random
import logging
try:
    import pifacedigitalio
    pfd = pifacedigitalio.PiFaceDigital()
    pfd_installed = True
except ImportError:
    pfd_installed = False

from threaded_timer import TimerControl

HIDE_MOUSE = True
RESETPIN = 0
GLOVETESTPIN = 1
OFFPIN = 2
STARTPIN = 3
HEADPHONEMAGNETPIN = 4
USE_HEADPHONE_SENSOR = True
QUIT_WITH_KEYBOARD = True
FULLSCREEN = False
FPS = 60
DEBUG = True
MOVIE_FILE='take3d.mpg'
SCREENSAVER_MESSAGE = 'Open box'
class QuitException(Exception):
    pass

def led_off(pin):
    # Wrappers for turn on/off LED by number
    pfd.leds[pin].turn_off()

def turn_off_all_outputs():
    [pfd.leds[i].turn_off() for i in range(0, 4)]
    pfd.relays[0].turn_off()
    pfd.relays[1].turn_off()

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
    time.sleep(4)
    pfd.relays[0].turn_off()
    pfd.relays[1].turn_off()


def play_main_movie():
    global movie
    movie.play()
    led_on(STARTPIN)

def reset_main_movie():
    global movie,screen
    led_on(RESETPIN)
    movie.rewind()
    blit_screen()
    screen.fill((0,0,0))
    time.sleep(0.5)
    play_main_movie()

def debug():
    if pfd_installed:
        logging.debug(
            ','.join(['%s:%s' %
                     (i, pfd.input_pins[i].value) for i in xrange(0,8)]
            )
        )


def check_keyboard_quit():
    if QUIT_WITH_KEYBOARD:
        if pygame.event.wait().type in (QUIT, KEYDOWN, MOUSEBUTTONDOWN):
            raise QuitException

def blit_screen():
    global screen,movie_screen,movie
    time.sleep(.001)
    screen.blit(movie_screen, (0, 0))
    logging.debug('frame: %s ' % movie.get_frame())
    pygame.display.update()

def headphones_on_stand():
    headphone_status = pfd.input_pins[HEADPHONEMAGNETPIN].value
    if DEBUG:
        logging.debug('headphone is on stand status: %s' % headphone_status)
    return headphone_status


def start_button_pressed():
    return pfd.input_pins[STARTPIN].value


def write_text(msg='Open Box'):
    wincolor = 40, 40, 90
    fg = 250, 240, 230
    bg = 5, 5, 5
    # fill background
    font = pygame.font.Font(None, 30)
    size = font.size(msg)
    ren = font.render(msg, 1, fg)
    screen.fill(wincolor)
    screen.blit(ren, (30 + size[0],
                      40 + size[1])
                )
    pygame.display.update()


def screensaver():
    """
        Waiting for a user. Waiting for the headphones to be lifted
    """
    print 'screensaver start'
    print 'wait for headphones to be lifted'
    global USE_HEADPHONE_SENSOR
    write_text(msg=SCREENSAVER_MESSAGE)
    while True:
        if DEBUG:
            logging.debug('screensaver phase')
        if USE_HEADPHONE_SENSOR:
            if not headphones_on_stand():
                print 'headphones lifted'
                time.sleep(1)
                return
        else:
            if start_button_pressed():
                print 'start button'
                time.sleep(1)
                return

def replace_headphones():
    write_text(msg='Return Headphones')

    print 'waiting for headphones to be reset'
    while True:
        if DEBUG:
            logging.debug('waiting for headphones to be reset phase')
        if USE_HEADPHONE_SENSOR:
            if start_button_pressed() or headphones_on_stand():
                print 'headphones reset'
                time.sleep(2)
                return
        else:
            time.sleep(3)
            print 'auto reset & start again'
            return


def start_mainmovie():
    if not USE_HEADPHONE_SENSOR:
        play_main_movie()
    while True:
        try:
            if DEBUG:
                logging.debug('---play---')
            blit_screen()
            clock.tick(FPS)
            if DEBUG:
                debug()
            if pfd.input_pins[RESETPIN].value:
                return
            if USE_HEADPHONE_SENSOR and headphones_on_stand():
                return
            if pfd.input_pins[GLOVETESTPIN].value:
                glovetest()
            if pfd.input_pins[OFFPIN].value:
                print 'ok, quit main movie'
                raise QuitException
            if start_button_pressed():
                play_main_movie()
        except Exception as err:
            raise


if __name__ == "__main__":
    pygame.init()
    pygame.display.init()
    pygame.mouse.set_visible(not HIDE_MOUSE)
    movie_screen = pygame.Surface((800, 480))
    movie = pygame.movie.Movie(MOVIE_FILE)
    pygame.event.set_allowed((QUIT, KEYDOWN))
    movie.set_display(movie_screen)
    movie.set_volume(0.99)
    clock = pygame.time.Clock()
    if FULLSCREEN:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((400,240), pygame.RESIZABLE)
    print 'screen : %s' % str(screen)
    print 'movie size: %s' % str(movie.get_size())
    try:
        while True:
            screensaver()
            start_mainmovie()
            replace_headphones()
    except QuitException:
        print 'bye!'
        turn_off_all_outputs()
