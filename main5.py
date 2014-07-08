import time
import pifacedigitalio
import threading
from threaded_timer import timer_control
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
def led_on(pin):
    pfd.leds[pin].turn_on()
def activate_glove():
        led_on(GLOVETESTPIN)
        timer_control(funktion=led_off,args=[GLOVETESTPIN]).start()

def glovetest():
    activate_glove()
def off():
    raise

def start():
    movie.play()
    led_on(STARTPIN)
    timer_control(funktion=led_off,args=[STARTPIN]).start()

def reset():
    global movie,screen
    led_on(RESETPIN)
    timer_control(funktion=led_off,args=[RESETPIN]).start()
    movie.rewind()
    blit_screen()
    screen.fill((0,0,0))
    movie.pause()

def debug():
    for i in range(0, 8):
        print i, ' ', pfd.input_pins[i].value,
    print


def turn_off_leds():
    [pfd.leds[i].turn_off() for i in range(0, 4)]

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
            turn_off_leds()
            exit()

pygame.init()
clock = pygame.time.Clock()
pygame.display.init()
movie_screen = pygame.Surface((600,500))
movie = pygame.movie.Movie('parkinsons.mpg')
movie.set_display(movie_screen)
pygame.mouse.set_visible(not HIDE_MOUSE)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
print screen
print movie.get_size()

start_project()




