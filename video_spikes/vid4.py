import pygame
from time import sleep
pygame.init()
screen = pygame.display.set_mode((320,240))
movie = pygame.movie.Movie("parkinsons.mpg")
movie.play()
already_paused = False
while True:
    if movie.get_frame() > 200 and not already_paused :
        movie.pause()
        sleep(7)
        already_paused = True
        movie.pause()
    if not(movie.get_busy()):
        print("rewind")
        already_paused = False
        movie.rewind()
        movie.play()
    if pygame.QUIT in [e.type for e in pygame.event.get()]:
        break