import RPi.GPIO as GPIO
import time
STARTBUTTON = 18
QUITBUTTON = 24
LED = 25 
GLOVE_ON = 250
GLOVE_OFF = 440
PAUSE_FRAME = 325
FULLSCREEN = True
MOUSE_LINKED = False
HIDE_MOUSE = True
PHOTO_SENSOR_TRIGGER_ON_GO_DARK = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(QUITBUTTON, GPIO.IN)
GPIO.setup(STARTBUTTON, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)
startinputValue = False
quit = False
done_pausing = False
import pygame
FPS = 60
# this reads a photo receptor (pin 22)
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN)

def photo(pin):
    reading = 0
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(pin, GPIO.IN)
    while (GPIO.input(pin) == GPIO.LOW):
        reading += 1
    return reading

def mousepos():
    r= pygame.mouse.get_pos()
    return r

pygame.init()
clock = pygame.time.Clock()
movie = pygame.movie.Movie('parkinsons.mpg')
pygame.mouse.set_visible(not HIDE_MOUSE)
if FULLSCREEN: 
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(movie.get_size())
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
    #screen.blit(movie_screen,(0,0))
    if MOUSE_LINKED:
        for event in pygame.event.get():
            pass
        mpos = mousepos()
        screen.fill((0,0,0))
    else:
        mpos = (0,0)
    screen.blit(movie_screen,mpos)
    pygame.display.update()
    clock.tick(FPS)
    quit = GPIO.input(QUITBUTTON)
    frame = movie.get_frame()
    #print frame
    if  frame > GLOVE_ON and frame<GLOVE_OFF:
        GPIO.output(LED,GPIO.HIGH)
    else:
        GPIO.output(LED, GPIO.LOW)

    if frame > PAUSE_FRAME and not done_pausing:
        while not done_pausing:
            photoreading = photo(22)
            print photoreading
            if (PHOTO_SENSOR_TRIGGER_ON_GO_DARK
             and  photoreading>500
              ) or (
             not PHOTO_SENSOR_TRIGGER_ON_GO_DARK 
             and photoreading <400 ) :
                done_pausing = True
                continue

    if quit:
        print 'bye'
        GPIO.cleanup()
        exit()

