import RPi.GPIO as GPIO
import time 

PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)

pwm = GPIO.PWM(PIN, 1000)
for _ in range(5):
    pwm.start(100)
    time.sleep(1)
    pwm.start(50)
    time.sleep(1)
    pwm.start(10)
    time.sleep(1)

GPIO.cleanup()
