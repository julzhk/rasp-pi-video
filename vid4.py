import pygame
from time import sleep
pygame.init()
screen = pygame.display.set_mode((320,240))
movie = pygame.movie.Movie("centaur_1.mpg")
movie.play()
while True:
    print(movie.get_frame())
    if movie.get_frame() == 200:
        movie.pause()
        sleep(7)
        movie.pause()
    if not(movie.get_busy()):
        print("rewind")
        movie.rewind()
        movie.play()
        print(movie.get_frame())
        print('has video ,',movie.has_video())
        print('size ,',movie.get_size())
    if pygame.QUIT in [e.type for e in pygame.event.get()]:
        break