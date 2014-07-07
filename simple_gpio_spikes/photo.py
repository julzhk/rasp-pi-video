import RPi.GPIO as GPIO
import time

# this reads a photo receptor (pin 22)
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN)

def photo(pin):
    reading = 0
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(pin, GPIO.IN)
    while (GPIO.input(pin) == GPIO.LOW):
        reading += 1 
    return reading

while True:
    print photo(22)
