import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(24,GPIO.IN)
GPIO.setup(25,GPIO.OUT)
status = False
while True:
    print GPIO.input(24)
    if GPIO.input(24) == status:
        status = True
        GPIO.output(25,GPIO.HIGH)
    else:
        status = False
        GPIO.output(25,GPIO.LOW)
    time.sleep(0.2)
