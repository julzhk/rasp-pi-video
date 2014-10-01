import pygame
from pygame import Surface
from pygame.locals import *
# Todo: remove font object from TextLine() , to TextWall(). Then share a list of font's with any line.

"""Example of multi-line text class, with alpha transparency."""
lorem = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed aliquet
tellus eros, eu faucibus dui. Phasellus eleifend, massa id ornare sodales, est urna
congue tellus, vitae varius metus nunc non enim. Mauris elementum, arcu vitae tempor euismod, justo turpis malesuada est, sed dictum nunc nulla nec mauris. Cras felis eros, elementum vitae sollicitudin in, elementum et augue. Proin eget nunc at dui congue pretium. Donec ut ipsum ut lacus mollis tristique. In pretium varius dui eu dictum.

Proin pulvinar metus nec mi semper semper. Pellentesque habitant morbi tristique
senectus et netus et malesuada fames ac turpis egestas. Proin in diam odio. Vestibulum
at neque sed ante sodales eleifend quis id dui. Mauris sollicitudin, metus a semper consectetur,
est lectus varius erat, sit amet ultrices tortor nisi id justo. Aliquam elementum vestibulum dui ut auctor. Mauris commodo sapien vitae augue tempus sagittis. Morbi a nibh lectus, sed porta nibh. Donec et est ac dui sodales aliquet tristique et arcu. Nullam enim felis, posuere vel rutrum eu, euismod a purus. Morbi porta cursus libero, id rutrum elit lacinia vitae.

In condimentum ultrices ipsum, ut convallis odio egestas et. Cras at egestas elit. Morbi
quis neque ligula. Sed tempor, sem at fringilla rhoncus, diam quam mollis nisi, vitae semper
mi massa sit amet tellus. Vivamus congue commodo ornare. Morbi et mi non sem malesuada rutrum. Etiam est purus, interdum ut placerat sit amet, tempus eget eros. Duis eget augue quis diam facilisis blandit. Ut vulputate adipiscing eleifend. """

class TextLine(object):
    # Manages drawing and caching a single line of text
    # You can make font size, .color_fg etc be properties so they *automatically* toggle dirty bool.
    def __init__(self, font=None, size=16, text="hi world"):        
        self.font_name = font
        self.font_size = size
        self.color_fg = Color("white")
        self.color_bg = Color("gray20")

        self._aa = True 
        self._text = text                
        self.font = pygame.font.Font(font, size)
        self.screen = pygame.display.get_surface()

        self.dirty = True
        self.image = None
        self._render()

    def _render(self):
        # render for cache
        """no AA = automatic transparent. With AA you need to set the color key too"""
        self.dirty = False        
        self.image = self.font.render(self._text, self.aa, self.color_fg)            
        self.rect = self.image.get_rect()

    def draw(self):
        # Call this do draw, always prefers to use cache
        if self.dirty or (self.image is None): self._render()
        self.screen.blit(self.image, self.rect)        

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self.dirty = True
        self._text = text

    @property
    def aa(self): return self._aa

    @aa.setter
    def aa(self, aa):
        self.dirty = True
        self._aa = aa

class TextWall(object):
    # Manages multiple lines of text / paragraphs.
    def __init__(self, font=None, size=16):
        self.font = font
        self.font_size = size        
        self.offset = Rect(20,20,1,1) # offset of whole wall

        self.screen = pygame.display.get_surface()
        self.dirty = True
        self.text_lines = []
        self._text_paragraph = "Empty\nText"
        self._render()

    def _render(self):
        # render list 
        self.dirty = False
        self.text_lines = [ TextLine(self.font, self.font_size, line) for line in self._text_paragraph ]        

        # offset whole paragraph
        self.text_lines[0].rect.top = self.offset.top

        # offset the height of each line
        prev = Rect(0,0,0,0)        
        for t in self.text_lines:
            t.rect.top += prev.bottom
            t.rect.left = self.offset.left
            prev = t.rect

    def parse_text(self, text):
        # parse raw text to something usable
        self._text_paragraph = text.split("\n")
        self._render()

    def draw(self):
        # draw with cached surfaces    
        if self.dirty: self._render()
        for text in self.text_lines: text.draw()

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, size):
        self.dirty = True
        self._font_size = size

    @property
    def text(self):
        return self._text_paragraph

    @text.setter
    def text(self, text_paragraph):
        self.dirty = True
        self.parse_text(text_paragraph)

class Game():
    done = False
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode ((640,480))
        self.text = Surface([200,100])

        self.text_wall = TextWall()
        self.toggle_bg = True

        self.text_wall.parse_text(lorem)

    def loop(self):
        while not self.done:
            self.handle_events()
            self.draw()

    def draw(self):
        if self.toggle_bg: bg = Color("gray60")
        else: bg = Color("gray20")

        self.screen.fill(bg)        
        self.text_wall.draw()        
        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.done = True

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE: self.done = True                
                elif event.key == K_SPACE: self.toggle_bg = not self.toggle_bg
                elif event.key == K_1: self.text_wall.font_size -= 3
                elif event.key == K_2: self.text_wall.font_size += 3

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    text = Surface([200,100])
    text_wall = TextWall()
    bg = (0,0,0)
    text_wall.parse_text(lorem)
    screen.fill(bg)
    text_wall.draw()
    pygame.display.update()
    import time
    time.sleep(7)
