import logging
import os
import sys
import time
import pexpect
import threading
import textwrap
try:
    import pygame
    import pifacedigitalio
    from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN
    from pygame import Surface
    from tbo import TBOPlayer
    from text_block import TextWall, TextLine
    piface_IO = pifacedigitalio.PiFaceDigital()
except ImportError:
    print 'running development environment'
    from mocks import pygame
    from mocks import piface_IO
    from mocks import TextWall, TextLine
    from mocks import TBOPlayer

#  log to file?
logging.basicConfig(filename='debuglog.log',level=logging.DEBUG)
logging.info("Current time %s" % time.strftime("%c"))

RESETPIN = 0
OFFPIN = 1
STARTPIN = 2
HEADPHONEPIN = 3
FULLSCREEN = True
SCREENSAVER_MESSAGE = 'Put on the headphones to start'
BUTTON_MESSAGE = "Listen to the instructions and press the red 'start' button  when ready"
RETURN_HEADPHONES_TO_STAND_MESSAGE = 'Please return headphones to the stand'

# how many seconds after the start of the movie should the glove start?
# GLOVE_COMMENCE_TIME = 150
GLOVE_COMMENCE_TIME = 10
# how many seconds after the start of the movie should the glove stop?
GLOVE_QUIT_TIME = 565
# off timecode: 9:25

DEBUG = True
LINE_CHAR_LEN = 30
INSTRUCTIONS_FILE = 'instructions.mp3'
# short clip! MOVIE_FILE = 'testc.mov'
MOVIE_FILE = 'transports.mp4'
GPIO_DEBUG = False
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
    logging.info('PhaseEnd Exception')
    pass


def led_off(pin):
    # Wrappers for turn on/off LED by number
    piface_IO.leds[pin].turn_off()

def turn_off_all_outputs():
    [piface_IO.leds[i].turn_off() for i in range(0, 4)]
    quit_glove()

def activate_glove():
    # turn on LED & turn on both Relays
    piface_IO.relays[0].turn_on()
    piface_IO.relays[1].turn_on()

def quit_glove():
    # turn on LED & turn off both Relays
    logging.info('glove relays off')
    piface_IO.relays[0].turn_off()
    piface_IO.relays[1].turn_off()

def play_movie(track):
    global omxplayer
    if DEBUG:
        logging.info('play %s track' % track)
    omxplayer = TBOPlayer()
    omxplayer.start_omx(track=track)
    time.sleep(1.5)

def play_main_movie():
    return play_movie(track=MOVIE_FILE)


def omxplayercounter():
    """
    How many omx players are running at the moment? Set into the
    GLOBAL VARIABLE: _OMXPLAYER_COUNT
    Found by doing a ps command & counting how many jobs return
    Sets itself up as a DAEMON, running every three seconds.
    """
    global _OMXPLAYER_COUNT, _videocountthread_running
    videocountthread = threading.Timer(3, omxplayercounter)
    if _videocountthread_running:
        videocountthread.start()
    omx_pids = pexpect.spawn('pgrep omxplayer')
    pslist = omx_pids.read().split()
    _OMXPLAYER_COUNT = len(pslist)
    logging.info('%s omx players' % _OMXPLAYER_COUNT )
    return videocountthread


def cleanup_omx_player():
    logging.info('clean up main movie called')
    omx_pids = pexpect.spawn('pgrep omxplayer')
    time.sleep(.25)
    pslist = omx_pids.read()
    logging.info( str(pslist))
    for pid in pslist.split():
        killcmd = pexpect.spawn('kill -9 %s' % pid)
        print killcmd.read()


def debug_gpio():
    if GPIO_DEBUG:
        logging.debug(
           ','.join(['%s:%s' %
                     (i, piface_IO.input_pins[i].value) for i in xrange(0, 8)]
           )
        )


def headphones_on_stand():
    headphone_status = piface_IO.input_pins[HEADPHONEPIN].value
    # if DEBUG:
    #     logging.debug('headphone is on stand status: %s' % headphone_status)
    return headphone_status


def start_button_pressed():
    return piface_IO.input_pins[STARTPIN].value


def write_text(msg='Demo message', wincolor=None, font_colour=None):
    if wincolor is None:
        wincolor = 0, 0, 0
    if font_colour is None:
        font_colour = 250, 240, 230
    msg = textwrap.fill(msg,LINE_CHAR_LEN)
    text_wall = TextWall(size=100)
    text_wall.parse_text(msg)
    screen.fill(wincolor)
    text_wall.draw()
    pygame.display.update()
    time.sleep(0.5)


def screensaver():
    """
        Waiting for a user. Waiting for the headphones to be lifted
    """
    logging.info( 'screensaver start')
    logging.info( 'wait for headphones to be lifted')
    write_text(msg=SCREENSAVER_MESSAGE)
    while True:
        quit_button_check()
        if not headphones_on_stand():
            logging.info('headphones lifted')
            time.sleep(0.25)
            return
        else:
            if start_button_pressed():
                logging.info('start button')
                time.sleep(0.25)
                return

def play_instructions():
    return play_movie(track=INSTRUCTIONS_FILE)


def replace_headphones():
    logging.info('waiting for headphones to be reset')
    write_text(msg=RETURN_HEADPHONES_TO_STAND_MESSAGE)
    wait = 0
    while wait < 15 and (start_button_pressed()==False) and (headphones_on_stand()==False):
        quit_button_check()
        print 'start button ', start_button_pressed()
        logging.info('headphones on stand status:' )
        logging.info(headphones_on_stand() )
        # logging.info( 'waiting for headphones reset')
        logging.info(wait)
        time.sleep(1)
        wait += 1
    logging.info('headphones reset phase done, start again')


def quit_button_check():
    reset_pin = piface_IO.input_pins[RESETPIN].value
    off_pin = piface_IO.input_pins[OFFPIN].value
    if reset_pin or off_pin:
        logging.info( 'ok, quit button')
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
    logging.info('stop watcher thread')


def start_mainmovie():
    write_text(msg=BUTTON_MESSAGE)
    start_pause = True
    quit_glove()
    while start_pause:
        quit_button_check()
        if start_button_pressed():
            cleanup_omx_player()
            time.sleep(1)
            play_main_movie()
            start_pause = False
    write_text(msg='')
    omxplayer_started = False
    starttime = time.time()
    quit_glove()
    while True:
        try:
            if DEBUG:
                logging.debug('videos: %s' % _OMXPLAYER_COUNT)
                debug_gpio()
            if _OMXPLAYER_COUNT >= 1:
                # it's got to start before the 'has ended' condition can apply
                omxplayer_started = True
            timecode = time.time() - starttime
            if timecode> GLOVE_COMMENCE_TIME and timecode < GLOVE_QUIT_TIME and not (int(timecode) % 5):
                # fire glove every n seconds between start and stop times
                logging.info('259:activate glove')
                activate_glove()
            elif timecode > GLOVE_QUIT_TIME and not (int(timecode) % 25):
                logging.info('262:off glove')
                quit_glove()
            if omxplayer_started and _OMXPLAYER_COUNT < 2:
                logging.info('video finished!')
                # so move to next phase
                raise PhaseEndException()
            if piface_IO.input_pins[RESETPIN].value:
                # so move to next phase
                raise PhaseEndException()
            if headphones_on_stand():
                raise PhaseEndException()
            quit_button_check()
            if start_button_pressed():
                pass
                # todo should exit / restart?
        except (QuitException, OffException):
            raise
        except PhaseEndException:
            return
        except Exception as err:
            logging.error('Unknown error: End video playing: %s' % err)


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
    cleanup_omx_player()
    quit_glove()

def exit_cleanup():
    logging.info( 'done!')
    cleanup()
    turn_off_all_outputs()
    quit_pygame_display()
    cleanup_omx_player()
    stop_omx_player_watcher_thread()



if __name__ == "__main__":
    start_py_game_display()
    try:
        while True:
            logging.info('1:start screensaver')
            screensaver()
            logging.info('2:play instruction')
            play_instructions()
            logging.info('3:start main movie')
            start_mainmovie()
            cleanup()
            logging.info('4:replace headphones')
            replace_headphones()
            logging.info('5:cleanup')
            cleanup()
    except QuitExc11eption:
        cleanup()
        logging.info( 'quit!')
        sys.exit()
    except OffException:
        exit_cleanup()
        logging.info( 'bye!')
        os.system("poweroff")
    except Exception as err:
        logging.info('Unexpected error')
        logging.info(type(err))
        logging.info(err.args)
        logging.info(err)
        exit_cleanup()
        logging.info('END')


