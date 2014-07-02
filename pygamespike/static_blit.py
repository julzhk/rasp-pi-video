#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
003_static_blit.py
static blitting and drawing
url: http://thepythongamebook.com/en:part2:pygame:step003
author: horst.jens@spielend-programmieren.at
licence: gpl, see http://www.gnu.org/licenses/gpl.html

Blitting a surface on a static position Drawing a filled circle into ballsurface.
Blitting this surface once. introducing pygame draw methods
The ball's rectangular surface is black because the background
color of the ball's surface was never defined nor filled."""
#the next line is only needed for python2.x and not necessary for python3.x
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
screen.blit(background, (0,0))     # blit the background on the screen (overwriting all)
screen.blit(movie_screen, (0,0))  # blit the topleft corner of ball surface at pos (ballx, bally)
clock = pygame.time.Clock()
mainloop = True
FPS = 30 # desired framerate in frames per second. try out other values !
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
    pygame.display.set_caption("Frame rate: %.2f frames per second. Playtime: %.2f seconds" % (clock.get_fps(),playtime))
    pygame.display.flip()          # flip the screen like in a flipbook
    pygame.display.update()
print( "this 'game' was played for %.2f seconds" % playtime)
