import RPi.GPIO as GPIO
import time 

PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)

for _ in range(5):
    GPIO.output(PIN, 1)
    time.sleep(1)
    GPIO.output(PIN, 0)
    time.sleep(1)

GPIO.cleanup()
