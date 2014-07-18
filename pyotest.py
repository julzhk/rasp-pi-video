from pyoplayer.pyomxplayer  import OMXPlayer
from pprint import pprint
omx = OMXPlayer('testb.mp4')
pprint(omx.__dict__)
omx.play()
omx.toggle_pause()
print omx.position
omx.stop()