import RPi.GPIO as GPIO
import time

# this reads a button(pin 24)

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN)
count = 0
while True:
    inputValue = GPIO.input(24)
    if (inputValue == True):
        count = count + 1
    print("Button pressed " + str(count) + " times.")
    time.sleep(.01)
