import RPi.GPIO as GPIO
import time 

PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)

GPIO.output(PIN, 1)
time.sleep(5)
GPIO.output(PIN, 0)
time.sleep(5)

GPIO.cleanup()
