import RPi.GPIO as GPIO
import time

swPin = 17
R = 14
G = 15
B = 18
LED_PINS = [R, G, B]

GPIO.setmode(GPIO.BCM)
GPIO.setup(swPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PINS, GPIO.OUT, initial=GPIO.LOW)

color_index = -1 

def button_callback(channel):
    global color_index

    # 간단한 소프트웨어 디바운스(10 ms)
    time.sleep(0.01)
    if GPIO.input(channel) == GPIO.HIGH:     # RISING 엣지 확인
        # 다음 색으로 이동
        color_index = (color_index + 1) % 4  # 0:R, 1:G, 2:B, 3:OFF

        # 모두 끄고
        GPIO.output(LED_PINS, GPIO.LOW)

        # 색상별로 켜기
        if color_index == 0:       # R
            GPIO.output(R, GPIO.HIGH)
        elif color_index == 1:     # G
            GPIO.output(G, GPIO.HIGH)
        elif color_index == 2:     # B
            GPIO.output(B, GPIO.HIGH)
        # color_index == 3 → OFF 그대로

        print(f"Button pressed → mode {color_index}")

#def printcallback(channel):
#	print("pushed")

GPIO.add_event_detect(swPin, GPIO.RISING, callback=button_callback, bouncetime=200)


try:
	while True:
		time.sleep(0.1)
except KeyboardInterrupt:
	pass
finally:
	GPIO.cleanup()
