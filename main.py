import time
import sys
import pygame
import pexpect
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN
import threading
from threading import Timer
import logging
from tbo import TBOPlayer
from pygame import Surface
from text_block import TextWall, TextLine
from threaded_timer import TimerControl

try:
    import pifacedigitalio
    pfd = pifacedigitalio.PiFaceDigital()
    pfd_installed = True
except ImportError:
    pfd_installed = False

# how many seconds after the start of the movie should the glove start?
# GLOVE_COMMENCE_TIME = 150
GLOVE_COMMENCE_TIME = 15
# how many seconds after the start of the movie should the glove stop?
# GLOVE_QUIT_TIME = 565
GLOVE_QUIT_TIME = 56
# off timecode: 9:25

RESETPIN = 0
GLOVETESTPIN = -1 # NOT ACCESSIBLE
OFFPIN = 1
STARTPIN = 2
HEADPHONEPIN = 3
FULLSCREEN = True
DEBUG = True
MOVIE_FILE = 'testb.mp4'
# short clip! MOVIE_FILE = 'testc.mov'
SCREENSAVER_MESSAGE = 'Put on the headphones to start'
BUTTON_MESSAGE = "Listen to the instructions, & press 'start' when ready"
RETURN_HEADPHONES_TO_STAND_MESSAGE = 'Please return headphones to the stand'
#  how many omx video threads are running at the moment?
#  will be 2 or 0
_OMXPLAYER_COUNT = None
_videocountthread_running = True


class QuitException(Exception):
    pass

class OffException(Exception):
    """
    Turn off the device
    """
    pass


class PhaseEndException(Exception):
    pass


def led_off(pin):
    # Wrappers for turn on/off LED by number
    pfd.leds[pin].turn_off()

def turn_off_all_outputs():
    [pfd.leds[i].turn_off() for i in range(0, 4)]
    quit_glove()


def led_on(pin):
    # Wrappers for turn on/off LED by number
    pfd.leds[pin].turn_on()
    # auto off LED in a few seconds
    TimerControl(funktion=led_off, args=[pin]).start()


def activate_glove():
    # turn on LED & turn on both Relays
    led_on(GLOVETESTPIN)
    pfd.relays[0].turn_on()
    pfd.relays[1].turn_on()


def quit_glove():
    # turn on LED & turn off both Relays
    led_off(GLOVETESTPIN)
    print 'relay0/1 off'
    pfd.relays[0].turn_off()
    pfd.relays[1].turn_off()


def glovetest():
    # called by button on pin GLOVETESTPIN
    activate_glove()
    time.sleep(2)
    quit_glove()


def play_main_movie():
    led_on(STARTPIN)
    global omxplayer
    if DEBUG:
        logging.info('play main movie..')
    omxplayer = TBOPlayer()
    omxplayer.start_omx(track=MOVIE_FILE)
    time.sleep(3)


def omxplayercounter():
    global _OMXPLAYER_COUNT, _videocountthread_running
    videocountthread = threading.Timer(3, omxplayercounter)
    if _videocountthread_running:
        videocountthread.start()
    omx_pids = pexpect.spawn('pgrep omxplayer')
    pslist = omx_pids.read().split()
    _OMXPLAYER_COUNT = len(pslist)


def cleanup_main_movie_player():
    print 'clean up main movie called'
    omx_pids = pexpect.spawn('pgrep omxplayer')
    time.sleep(1)
    pslist = omx_pids.read()
    print str(pslist)
    for pid in pslist.split():
        killcmd = pexpect.spawn('kill -9 %s' % pid)
        print killcmd.read()


def debug_gpio():
    if pfd_installed:
        logging.debug(
            ','.join(['%s:%s' %
                      (i, pfd.input_pins[i].value) for i in xrange(0, 8)]
            )
        )


def headphones_on_stand():
    headphone_status = pfd.input_pins[HEADPHONEPIN].value
    if DEBUG:
        logging.debug('headphone is on stand status: %s' % headphone_status)
    return headphone_status


def start_button_pressed():
    return pfd.input_pins[STARTPIN].value


def write_text(msg='Demo message', wincolor=None, font_colour=None):
    if wincolor is None:
        wincolor = 0, 0, 0
    if font_colour is None:
        font_colour = 250, 240, 230

    text_wall = TextWall()
    text_wall.parse_text(msg)
    screen.fill(wincolor)
    text_wall.draw()
    pygame.display.update()
    time.sleep(0.5)


def screensaver():
    """
        Waiting for a user. Waiting for the headphones to be lifted
    """
    print 'screensaver start'
    print 'wait for headphones to be lifted'
    write_text(msg=SCREENSAVER_MESSAGE)
    while True:
        quit_button_check()
        if DEBUG:
            logging.debug('screensaver phase')
        if pfd.input_pins[GLOVETESTPIN].value:
            glovetest()
        if not headphones_on_stand():
            print 'headphones lifted'
            time.sleep(0.5)
            return
        else:
            if start_button_pressed():
                print 'start button'
                time.sleep(0.5)
                return


def replace_headphones():
    print 'waiting for headphones to be reset'
    write_text(msg=RETURN_HEADPHONES_TO_STAND_MESSAGE)
    wait = 0
    while True:
        quit_button_check()
        if pfd.input_pins[GLOVETESTPIN].value:
            glovetest()
        if DEBUG:
            logging.debug('waiting for headphones to be reset phase')
        while wait > 15 or not (start_button_pressed() or headphones_on_stand()):
            print 'waiting for headphones reset'
            time.sleep(2)
            wait += 1
            return
        else:
            time.sleep(2)
            print 'headphones reset phase done, start again'
            return


def glove_handler():
    """
    starts and stops the glove at certain time stamps; using threads.

    """
    glove_start_thread = Timer(GLOVE_COMMENCE_TIME, activate_glove)
    glove_start_thread.start()  # after NN seconds, glove trembles
    glove_stop_thread = Timer(GLOVE_QUIT_TIME, quit_glove)
    glove_stop_thread.start()
    return glove_start_thread, glove_stop_thread


def quit_button_check():
    reset_pin = pfd.input_pins[RESETPIN].value
    off_pin = pfd.input_pins[OFFPIN].value
    if reset_pin or off_pin:
        print 'ok, quit button'
        quit_glove()
        if reset_pin:
            raise QuitException()
        if off_pin:
            raise OffException()


def stop_omx_player_watcher_thread():
    """
    This global variable is passed into the thread;
    if false the next thread doesn't start
    """
    global _videocountthread_running
    _videocountthread_running = False


def start_mainmovie():

    write_text(msg=BUTTON_MESSAGE)
    start_pause = True
    while start_pause:
        quit_button_check()
        if start_button_pressed():
            play_main_movie()
            start_pause = False
    write_text(msg='')
    glovestartthread, glovestopthread = glove_handler()
    omxplayer_started = False
    while True:
        try:
            if DEBUG:
                logging.debug('---play---')
                logging.debug('videos: %s' % _OMXPLAYER_COUNT)
                debug_gpio()
            if _OMXPLAYER_COUNT >= 1:
                # it's got to start before the 'has ended' condition can apply
                omxplayer_started = True
            if omxplayer_started and _OMXPLAYER_COUNT < 2:
                print 'video finished!'
                # so move to next phase
                raise PhaseEndException()
            if pfd.input_pins[RESETPIN].value:
                led_on(RESETPIN)
                # so move to next phase
                raise PhaseEndException()
            if headphones_on_stand():
                raise PhaseEndException()
            quit_button_check()
            if pfd.input_pins[GLOVETESTPIN].value:
                glovetest()
            if start_button_pressed():
                pass
                # todo should exit / restart?
        except PhaseEndException:
            cleanup_main_movie_player()
            glovestartthread.cancel()
            glovestopthread.cancel()
            quit_glove()
            return
        except Exception as err:
            print err
            raise


def start_py_game_display():
    global screen
    pygame.init()
    pygame.mixer.quit()
    pygame.display.init()
    pygame.font.init()
    pygame.mouse.set_visible(False)
    if FULLSCREEN:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((400, 240), pygame.RESIZABLE)


def quit_pygame_display():
    pygame.quit()


def cleanup():
    print 'done!'
    quit_pygame_display()
    cleanup_main_movie_player()
    stop_omx_player_watcher_thread()
    turn_off_all_outputs()


if __name__ == "__main__":
    start_py_game_display()
    omxplayercounter()
    try:
        while True:
            screensaver()
            start_mainmovie()
            replace_headphones()
            cleanup_main_movie_player()
    except QuitException:
        cleanup()
        print 'quit!'
        sys.exit()
    except OffException:
        cleanup()
        print 'bye!'
        import os
        os.system("poweroff")
