import time
STARTBUTTON = 18
QUITBUTTON = 24
LED = 25 
GLOVE_ON = 250
GLOVE_OFF = 440
PAUSE_FRAME = 325
FULLSCREEN = False
MOUSE_LINKED = True
HIDE_MOUSE = False

startinputValue = False
quit = False
done_pausing = False
import pygame
FPS = 60
def mousepos():
    r= pygame.mouse.get_pos()
    return r

pygame.init()
clock = pygame.time.Clock()
movie = pygame.movie.Movie('parkinsons.mpg')
pygame.mouse.set_visible(not HIDE_MOUSE)
#    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.init()
print movie.get_size()
# this is the viewport size
screen = pygame.display.set_mode((300,400), pygame.RESIZABLE)
movie_screen = pygame.Surface((600,500))
print screen
movie.set_display(movie_screen)
movie.play()
running = True
while running:
    time.sleep(.01)
    #screen.blit(movie_screen,(0,0))
    if MOUSE_LINKED:
        for event in pygame.event.get():
            pass
        mpos = mousepos() 
        mpos = [mpos[0] - 130, mpos[1] - 140 ]
        screen.fill((0,0,0))
    else:
        mpos = (0,0)
    screen.blit(movie_screen,mpos)
    pygame.display.update()
    clock.tick(FPS)
    frame = movie.get_frame()


