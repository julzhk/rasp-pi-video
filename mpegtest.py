import pygame
MOVIE_FILE = 'testb.mpg'
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.quit()
    pygame.display.init()
    movie_screen = pygame.Surface((800, 600))
    movie = pygame.movie.Movie(MOVIE_FILE)
    movie.set_display(movie_screen)
    movie.set_volume(0.99)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    print 'screen : %s' % str(screen)
    print 'movie size: %s' % str(movie.get_size())
    movie.rewind()
    movie.play()