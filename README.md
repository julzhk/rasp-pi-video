Raspberry Pi Video & Hardware controller
=============

This project (& it's investigation) gets a video player to play smoothly & full-screen. It's controlled via some Piface I/O controls: for instance to start, stop & reset the video player. It also triggers some hardware (a glove in this project) at particular timecodes in the video, these also are piface I/O events.

Notes:
- Text instructions use the Pygame library. I spent quite a bit of time coaxing Pygame to play video full screen & fast enough, but unfortunately it wasn't really up to it. But it makes it easy to write manipulate text on the screen easily.
- It uses the great TBO player library to spawn an OMX player on the Raspberry Pi. The TBO library plays via the Raspberry Pi Speakers; This project needs sound via the headphones, hence this library calls the OMX player with some different switch options.
- At end of the video loop the OMX player process is killed using the OS 'kill' command. This uses the pexpect library to issue a 'pgrep omxplayer' to get the PIDs of all (and there should be only one) OMX processes. Then it does a 'kill -9' on each of these PIDs.
- To trigger hardware events and have them persist for a while the project uses threads: ie: The project spawns a sub-process with a timer. When the timer expires, the hardware event resets & the thread exits. (see the TimerControl class)
- Optimizing videos: Some videos appear to have too high a bandwidth to play all the way through in OMX player: They'd get to a particular bit of the mpeg video & crash the player. Using ffMpeg, it's easy (but a bit slow!) to transcode to a lower bandwidth.

Some notes on working in the Raspberry Pi
=========

I use the fantastic Pycharm IDE on my Mac, and it took a while to get an efficient workflow in place: here's some notes on what I found:

- The large number of git commits is due to using git for deployment: ie check in to github & pull the changes to the Raspberry Pi. Although this is isn't too inefficient, it's not great for tweaking settings.
- Better: ssh into the raspberry pi. Use 'Chicken of the VNC' to view the Pi's desktop. Not really that useful, but handy sometimes.
- Once you have a ssh into the Raspberry Pi, set Pycharm to use the raspberry Pi's remote debugging: http://www.jetbrains.com/pycharm/webhelp/remote-debugging.html . This lets you run the python in the IDE, but use the Raspberry Pi's Python. 
- Register the ssh keys on the Raspberry Pi with your github account. Then if you make any changes on the Raspberry Pi directly, you can easily push them back into the github project.


Development Notes
=======

- debug process: login and run from another machine: ssh -Y pi@192.168.0.8
- then run: 
   cd rasp-pi-video/ 
   python main.py
   
- In another ssh shell: tail -f /rasp-pi-video/parkinsons.log