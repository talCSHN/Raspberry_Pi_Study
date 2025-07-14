import RPi.GPIO as GPIO, time

RED, GREEN, BLUE = 14, 15, 18
BUTTON, PIEZO = 17, 25
# COLORS = [RED, GREEN, BLUE]
LED_SEQ = { 'LOW' : RED, 'HIGH' : BLUE }

GPIO.setmode(GPIO.BCM)
GPIO.setup([RED, BLUE], GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIEZO, GPIO.OUT)

sound = GPIO.PWM(PIEZO, 700)

TONE_LOW = 650
TONE_HIGH = 900
DURATION = 0.4

def leds_off():
	GPIO.output([RED, BLUE], GPIO.HIGH)

def play_tone(freq, led_pin):
	sound.ChangeFrequency(freq)
	sound.ChangeDutyCycle(50)
	leds_off()
	GPIO.output(led_pin, GPIO.LOW)

try:
    playing = False
    next_time = 0
    state = 'LOW'
    prev_btn = GPIO.input(BUTTON)

    while True:
        now = time.monotonic()
        cur_btn = GPIO.input(BUTTON)

        # ─ 버튼 토글 ─
        if prev_btn and not cur_btn:
            if not playing:
                print("사이렌 ON")
                sound.start(50)
                playing, next_time, state = True, now, 'LOW'
            else:
                print("사이렌 OFF")
                playing = False
                sound.stop(); leds_off()
        prev_btn = cur_btn

        # ─ 사이렌 루프 ─
        if playing and now >= next_time:
            if state == 'LOW':
                play_tone(TONE_LOW, LED_SEQ['LOW'])
                state = 'HIGH'
            else:
                play_tone(TONE_HIGH, LED_SEQ['HIGH'])
                state = 'LOW'
            next_time = now + DURATION

        time.sleep(0.002)

except KeyboardInterrupt:
    pass
finally:
    sound.stop()
    leds_off()
    GPIO.cleanup()
    print("종료")


