global movie
import pygame
pygame.init()
movie = pygame.movie.Movie("take3e.mpg")
if movie.has_video():
    screen = pygame.display.set_mode(movie.get_size())
    movie_length = movie.get_length()
    movie.set_volume(0.99)
    movie.set_display(screen)
    movie.play()
