Raspberry Pi Video & Hardware controller
=============

This project (& it's investigation) gets a video player to play smoothly & full-screen. It's controlled via some Piface I/O controls: for instance to start, stop & reset the video player. It also triggers some hardware (a glove in this project) at particular timecodes in the video, these also are piface I/O events.

Notes:
- Text instructions use the Pygame library. I spent quite a bit of time coaxing Pygame to play video full screen & fast enough, but unfortunately it wasn't really up to it. But it makes it easy to write manipulate text on the screen easily.
- It uses the great TBO player library to spawn an OMX player on the Raspberry Pi. The TBO library plays via the Raspberry Pi Speakers; This project needs sound via the headphones, hence this library calls the OMX player with some different switch options.
- At end of the video loop the OMX player process is killed using the OS 'kill' command. This uses the pexpect library to issue a 'pgrep omxplayer' to get the PIDs of all (and there should be only one) OMX processes. Then it does a 'kill -9' on each of these PIDs.
- To trigger hardware events and have them persist for a while the project uses threads: ie: The project spawns a sub-process with a timer. When the timer expires, the hardware event resets & the thread exits. (see the TimerControl class)
