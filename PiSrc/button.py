import RPi.GPIO as GPIO
import time

buttonPin = 17

GPIO.setmode(GPIO.BCM)

# GPIO.setup(buttonPin, GPIN.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(buttonPin, GPIO.IN)

is_pressed = False

try:
	while True:
		if(GPIO.input(buttonPin)):
			if(is_pressed == False):
				print("waiting")
			is_pressed = True
		else:
			if(is_pressed == True):
					print("button pressed")
					is_pressed = False
		# print(f'debug : {is_pressed}')
		time.sleep(1)
except KeyboardInterrupt:
	GPIO.cleanup()
