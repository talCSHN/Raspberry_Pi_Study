from flask import Flask
import RPi.GPIO as GPIO

app = Flask(__name__)

R = 14
G = 15
B = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup([R, G, B], GPIO.OUT)

@app.route('/')
def ledFlask():
	return 'LED Control Web'

@app.route('/led/<color>/<state>')
def led(color, state):
	if state == 'on':
		if color == 'red':
			GPIO.output(G, GPIO.HIGH)
			GPIO.output(B, GPIO.HIGH)
			GPIO.output(R, GPIO.LOW)
		elif color == 'green':
			GPIO.output(R, GPIO.HIGH)
			GPIO.output(B, GPIO.HIGH)
			GPIO.output(G, GPIO.LOW)
		elif color == 'blue':
			GPIO.output(R, GPIO.HIGH)
			GPIO.output(G, GPIO.HIGH)
			GPIO.output(B, GPIO.LOW)
	else:
			GPIO.output(R, GPIO.HIGH)
			GPIO.output(G, GPIO.HIGH)
			GPIO.output(B, GPIO.HIGH)

	return f'{color} + {state}'

@app.route('/led/clean')
def gpio_clean_up():
	GPIO.cleanup()
	return '<h1>GPIO CLEAN UP</h1>'

if __name__ == '__main__':
	app.run(host='0.0.0.0')
