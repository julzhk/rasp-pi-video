import time
import pifacedigitalio

pfd = pifacedigitalio.PiFaceDigital()
import pygame

HIDE_MOUSE = True
RESETPIN = 0
GLOVETESTPIN = 1
OFFPIN = 2
STARTPIN = 3
FPS = 60
DEBUG = True


def activate_glove():
    pass
    pfd.output_pin(GLOVETESTPIN).value = 1


def reset():
    pass
    pfd.output_pin(RESETPIN).value = 1


def glovetest():
    activate_glove()
    pfd.output_pin(GLOVETESTPIN).value = 1


def off():
    pfd.output_pin(OFFPIN).value = 1
    exit()
def start():
    pass
    pfd.output_pin(STARTPIN).value = 1
def debug():
    for i in range(0, 8):
        print i, ' ', pfd.input_pins[i].value,
    print
pygame.init()
clock = pygame.time.Clock()
movie = pygame.movie.Movie('parkinsons.mpg')
pygame.mouse.set_visible(not HIDE_MOUSE)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
print screen
pygame.display.init()
print movie.get_size()
movie_screen = pygame.Surface((600,500))
movie.set_display(movie_screen)
movie.play()
while True:
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




