from omxwrapper import OMXPlayer
from pprint import pprint
import pdb
omx = OMXPlayer('take3n.mp4')
pprint(omx.__dict__)
print omx.position
omx.stop()