import RPi.GPIO as GPIO
import time

# this reads a button(pin 17
# reading a hall - effect magnetometer
# pin 1 : power
# pin 2 : grnd
# pin 3 : 10k pull up resistor PLUS to pin

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
count = 0
while True:
    inputValue = GPIO.input(17)
    print inputValue
    time.sleep(.01)
