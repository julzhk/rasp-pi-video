import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT)
GPIO.setup(24,GPIO.IN)
while True:
    GPIO.output(25,GPIO.HIGH)
    print GPIO.input(24)
    time.sleep(1)
    GPIO.output(25,GPIO.LOW)
    time.sleep(1)
