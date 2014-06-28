import RPi.GPIO as GPIO
import time
STARTBUTTON = 18
QUITBUTTON = 24
LED = 25 
GLOVE_ON = 250
GLOVE_OFF = 440
GPIO.setmode(GPIO.BCM)
GPIO.setup(QUITBUTTON, GPIO.IN)
GPIO.setup(STARTBUTTON, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)
startinputValue = False
quit = False
import pygame
FPS = 60
pygame.init()
clock = pygame.time.Clock()
movie = pygame.movie.Movie('parkinsons.mpg')
#screen = pygame.display.set_mode(movie.get_size())
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
movie_screen = pygame.Surface(movie.get_size()).convert()
print screen
movie.set_display(movie_screen)
movie.play()
running = True
while running:
    time.sleep(.01)
    startinputValue = startinputValue or GPIO.input(STARTBUTTON)
    # dont do anything until the button pressed
    if (not startinputValue):
        continue
    startinputValue = True
    screen.blit(movie_screen,(110,110))
    pygame.display.update()
    clock.tick(FPS)
    quit = GPIO.input(QUITBUTTON)
    frame = movie.get_frame()
    print frame
    if  frame > GLOVE_ON and frame<GLOVE_OFF:
        GPIO.output(LED,GPIO.HIGH)
    else:
        GPIO.output(LED, GPIO.LOW)
    if quit:
        print 'bye'
        GPIO.cleanup()
        exit()

