#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division
import pygame
pygame.init()
screen=pygame.display.set_mode((640,480))
background = pygame.Surface(screen.get_size())
background.fill((255,255,255))     # fill the background white (red,green,blue)
background = background.convert()  # faster blitting
ballsurface = pygame.Surface((50,50))     # create a rectangular surface for the ball
#pygame.draw.circle(Surface, color, pos, radius, width=0) # from pygame.org documentation
pygame.draw.circle(ballsurface, (0,0,255), (25,25),25) # draw blue filled circle on ball surface
ballsurface = ballsurface.convert()              # faster blitting
movie = pygame.movie.Movie('parkinsons.mpg')
movie_screen = pygame.Surface(movie.get_size()).convert()
movie.play()
import time
screen.blit(movie_screen, (0,0))  # blit the topleft corner of ball surface at pos (ballx, bally)
clock = pygame.time.Clock()
mainloop = True
FPS = 10 # desired framerate in frames per second. try out other values !
playtime = 0.0
def mousepos():
    r= pygame.mouse.get_pos()
    return r
while mainloop:
    mpos = mousepos()
    screen.fill((0,0,0))
    screen.blit(background,mpos)
    screen.blit(movie_screen,mpos)
    milliseconds = clock.tick(FPS) # do not go faster than this frame rate
    playtime += milliseconds / 1000.0
    # ----- event handler -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False # pygame window closed by user
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False # user pressed ESC
    try:
        pygame.display.set_caption("Frame rate: %.2f frames per second. Playtime: %.2f seconds" % (clock.get_fps(),playtime))
        pygame.display.update()
    except:
        print( 'oopsy'),
print( "this 'game' was played for %.2f seconds" % playtime)
