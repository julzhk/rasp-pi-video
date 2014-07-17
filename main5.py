import time
import pygame
import logging_data
import logging_decorator
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
FULLSCREEN = False
FPS = 60
DEBUG = True
MOVIE_FILE='Take3d.mpg'

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
    movie.pause()

def debug():
    if pfd_installed:
        logging.debug(','.join(['%s:%s' % (i, pfd.input_pins[i].value) for i in xrange(0,8)]))


def blit_screen():
    global screen,movie_screen,movie
    time.sleep(.001)
    screen.blit(movie_screen, (0, 0))
    logging.debug('frame: %s ' % movie.get_frame())
    pygame.display.update()


def screensaver():
    """
        Waiting for a user. Waiting for the headphones to be lifted
    """
    print 'screensaver start'
    print 'wait for headphones to be lifted'
    while True:
        if pfd.input_pins[STARTPIN].value or pfd.input_pins[HEADPHONEMAGNETPIN].value:
            print 'headphones lifted'
            return

def replace_headphones():
    print 'waiting for headphones to be reset'
    while True:
        if pfd.input_pins[STARTPIN].value or not pfd.input_pins[HEADPHONEMAGNETPIN].value:
            print 'headphones reset'
            return

    print 'headphones reset'

def start_mainmovie():
    while True:
        try:
            blit_screen()
            clock.tick(FPS)
            if DEBUG:
                debug()
            if pfd.input_pins[RESETPIN].value:
                reset_main_movie()
            if pfd.input_pins[GLOVETESTPIN].value:
                glovetest()
            if pfd.input_pins[OFFPIN].value:
                print 'ok, quit main movie'
                raise QuitException
            if pfd.input_pins[STARTPIN].value:
                play_main_movie()
        except Exception as err:
            raise


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
    try:
        while True:
            screensaver()
            start_mainmovie()
            replace_headphones()
    except QuitException:
        print 'bye!'
        turn_off_all_outputs()
