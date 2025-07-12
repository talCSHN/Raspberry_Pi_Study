import RPi.GPIO as GPIO
import time

try:
	while(1):
		GPIO.setmode(GPIO.BCM)
		RED = 14
		GPIO.setup(RED, GPIO.OUT)
		GPIO.output(RED, GPIO.LOW)
		time.sleep(1)
		GPIO.cleanup()

		GPIO.setmode(GPIO.BCM)
		GREEN = 15
		GPIO.setup(GREEN, GPIO.OUT)
		GPIO.output(GREEN, GPIO.LOW)
		time.sleep(1)
		GPIO.cleanup()

		GPIO.setmode(GPIO.BCM)
		BLUE = 18
		GPIO.setup(BLUE, GPIO.OUT)
		GPIO.output(BLUE, GPIO.LOW)
		time.sleep(1)
		GPIO.cleanup()

finally:
	GPIO.cleanup()
