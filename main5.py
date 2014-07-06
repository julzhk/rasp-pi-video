import time

HIDE_MOUSE = True
import pygame
FPS = 60
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


