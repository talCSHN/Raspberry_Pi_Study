import RPi.GPIO as GPIO
import time

RED = 14
GREEN = 15
BLUE = 18
BUTTON = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup([RED, GREEN, BLUE], GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_UP)

press_count = 0
prev_input = GPIO.input(BUTTON)

def set_rgb(r=False, g=False, b=False):
	if r:
		GPIO.output(RED, GPIO.LOW)
	else:
		GPIO.output(RED, GPIO.HIGH)
	if g:
		GPIO.output(GREEN, GPIO.LOW)
	else:
		GPIO.output(GREEN, GPIO.HIGH)
	if b:
		GPIO.output(BLUE, GPIO.LOW)
	else:
		GPIO.output(BLUE, GPIO.HIGH)

try:
	while True:
		curr_input = GPIO.input(BUTTON)

		if (prev_input == GPIO.HIGH and curr_input == GPIO.LOW):
			press_count += 1

			if (press_count == 1):
				set_rgb(r=True)
				print('RED')
			elif (press_count == 2):
				set_rgb(g=True)
				print('GREEN')
			elif (press_count == 3):
				set_rgb(b=True)
				print('BLUE')
			elif (press_count == 4):
				set_rgb()
				print('LED OFF')
				press_count = 0

		prev_input = curr_input
		time.sleep(0.1)

except KeyboardInterrupt:
	GPIO.cleanup()
