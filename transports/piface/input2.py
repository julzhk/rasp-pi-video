import pifacedigitalio
import os
def toggle_led0(event):
    event.chip.leds[0].toggle()

def play_video(event):
    print 'start video'

def reset_video(event):
    print 'reset video'

def glove_test(event):
    print 'glove test'

def quit(event):
    ''' will be a shutdown command
    '''
    os.system("shutdown -h 0")

p = pifacedigitalio.PiFaceDigital()
l0 = pifacedigitalio.InputEventListener(chip=p)
l1 = pifacedigitalio.InputEventListener(chip=p)
l2 = pifacedigitalio.InputEventListener(chip=p)
l3 = pifacedigitalio.InputEventListener(chip=p)

l3.register(3,pifacedigitalio.IODIR_FALLING_EDGE,play_video)
l0.register(0,pifacedigitalio.IODIR_FALLING_EDGE,reset_video)
l1.register(1,pifacedigitalio.IODIR_FALLING_EDGE, glove_test)
l2.register(2,pifacedigitalio.IODIR_FALLING_EDGE, quit)

l0.activate()
l1.activate()
l2.activate()
l3.activate()
