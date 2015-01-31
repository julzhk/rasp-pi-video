from mock import MagicMock
import logging

class PyGame(object):
    FULLSCREEN = '1080p'
    RESIZABLE = False

class Display(object):
    pass

pygame = PyGame()
pygame.display = MagicMock(return_value=1)
pygame.display.set_mode = MagicMock()
pygame.display.set_mode.fill = MagicMock(return_value=2.2)
pygame.screen = MagicMock(return_value=2.5)
pygame.screen.fill = MagicMock(return_value=2.75)
pygame.init = MagicMock(return_value=3)
pygame.quit = MagicMock(return_value=4)
pygame.mixer = MagicMock(return_value=5)
pygame.mixer.quit = MagicMock(return_value=6)
pygame.font = MagicMock(return_value=7)
pygame.font.init = MagicMock(return_value=8)
pygame.mouse = MagicMock(return_value=9)
pygame.mouse.set_visible = MagicMock(return_value=10)
pygame.display.update= MagicMock(return_value=11)

class Piface_IO(object):
    input_pins = {}
    for i in range(-10,10):
        input_pins[i] = MagicMock(value=False)
    # PUSHING THE START BUTTON
    input_pins[2] = MagicMock(value=True)
piface_IO = Piface_IO()
piface_IO.leds= MagicMock(return_value=3)
piface_IO.relays= MagicMock(return_value=3)

class TextWall(object):
    pass
TextWall.__init__= MagicMock(return_value=None)
TextWall.parse_text = MagicMock(return_value=12)
TextWall.draw = MagicMock(return_value=13)

class TextLine(object):
    pass

def write_text(msg,*args, **kwargs):
    print msg
    logging.info(msg)

TBOPlayer = MagicMock()
TBOPlayer.start_omx = MagicMock()