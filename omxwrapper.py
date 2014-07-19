import pexpect
import re

from threading import Thread
from time import sleep

class OMXPlayer(object):

    _STATUS_REXP = re.compile(r"V :\s*([\d.]+).*")
    _DONE_REXP = re.compile(r"have a nice day.*")
    _LAUNCH_CMD = '/usr/bin/omxplayer -s %s %s'
    _PAUSE_CMD = 'p'
    _TOGGLE_SUB_CMD = 's'
    _QUIT_CMD = 'q'

    paused = False
    subtitles_visible = True

    def __init__(self, mediafile, args="", start_playback=False):
        cmd = self._LAUNCH_CMD % (mediafile, args)
        self._process = pexpect.spawn(cmd)
        self._position_thread = Thread(target=self._get_position)
        self._position_thread.start()


    def _get_position(self):
        while True:
            index = self._process.expect([self._STATUS_REXP,
                                            pexpect.TIMEOUT,
                                            pexpect.EOF,
                                            self._DONE_REXP])
            self.position = float(self._process.match.group(1))
            sleep(0.05)

    def toggle_pause(self):
        if self._process.send(self._PAUSE_CMD):
            self.paused = not self.paused

    def stop(self):
        self._process.send(self._QUIT_CMD)
        self._process.terminate(force=True)
