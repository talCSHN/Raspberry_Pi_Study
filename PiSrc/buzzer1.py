import RPi.GPIO as GPIO
import time

buzzerPin = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzerPin, GPIO.OUT)

try:
	GPIO.output(buzzerPin, GPIO.HIGH)
	print("Buzzer On")
	time.sleep(1)
	GPIO.output(buzzerPin, GPIO.LOW)
	print("Buzzer Off")

except KeyboardInterrupt:
	print("End")
finally:
	GPIO.cleanup()
