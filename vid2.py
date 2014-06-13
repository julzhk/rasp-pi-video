import pygame
from time import sleep
pygame.init()
screen = pygame.display.set_mode((320,240))
movie = pygame.movie.Movie("centaur_1.mpg")
movie.play()
while True:
    if not(movie.get_busy()):
        print("rewind")
        movie.rewind()
        movie.play()
        print(movie.get_frame())
    if pygame.QUIT in [e.type for e in pygame.event.get()]:
        break