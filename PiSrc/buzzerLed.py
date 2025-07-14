import RPi.GPIO as GPIO, time


RED, GREEN, BLUE = 14, 15, 18
BUTTON           = 17
PIEZO            = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup([RED, GREEN, BLUE], GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(PIEZO, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pwm = GPIO.PWM(PIEZO, 440)

MELODY = [
    ('E4',0.5),('F4',0.5),('G4',0.25),('A4',0.25),
    ('G4',0.25),('F4',0.25),('E4',0.5),('D4',0.5),
    ('C4',1.0),('E4',1.0)
]
FREQS = {'C4':261,'D4':294,'E4':329,'F4':349,'G4':392,'A4':440}
BEAT  = 60 / 143

COLORS = [RED, GREEN, BLUE]

def led_off(): GPIO.output([RED,GREEN,BLUE], GPIO.HIGH)

playing   = False
note_idx  = 0
note_end  = 0

prev_btn  = GPIO.input(BUTTON)

try:
    while True:
        now = time.monotonic()
        curr_btn = GPIO.input(BUTTON)
        if prev_btn==GPIO.HIGH and curr_btn==GPIO.LOW:
            if not playing:
                playing  = True
                note_idx = 0
                note_end = now
                pwm.start(50)
                print("PLAY")
            else:
                playing = False
                pwm.stop()
                led_off()
                print("STOP")
        prev_btn = curr_btn

        if playing and now >= note_end:
            if note_idx < len(MELODY):
                note, length = MELODY[note_idx]
                pwm.ChangeFrequency(FREQS[note])
                led_off()
                GPIO.output(COLORS[note_idx % 3], GPIO.LOW)
                note_end = now + length * BEAT
                note_idx += 1
            else:
                playing = False
                pwm.stop()
                led_off()
                print("END")

        time.sleep(0.01)

except KeyboardInterrupt:
    pwm.stop()
    led_off()
    GPIO.cleanup()
