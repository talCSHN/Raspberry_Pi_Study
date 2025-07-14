import RPi.GPIO as GPIO, time

# ─ GPIO 설정 ─
RED, GREEN, BLUE = 14, 15, 18
BUTTON, PIEZO = 17, 25
COLORS = [RED, GREEN, BLUE]

GPIO.setmode(GPIO.BCM)
GPIO.setup(COLORS, GPIO.OUT, initial=GPIO.HIGH)   # HIGH=LED off
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIEZO,  GPIO.OUT)

pwm = GPIO.PWM(PIEZO, 440)     # dummy freq, 시작 시 start() 안 함

# ─ 주파수 테이블 ─
FREQ = {
    'REST': 0,
    'C4':262,'Cs4':277,'D4':294,'Ds4':311,'E4':330,'F4':349,'Fs4':370,
    'G4':392,'Gs4':415,'A4':440,'As4':466,'B4':494,
    'C5':523,'Cs5':554,'D5':587,'Ds5':622,'E5':659,'F5':698,'Fs5':740,
    'G5':784,'Gs5':831,'A5':880,'As5':932,'B5':988
}

# ─ 멜로디 ─
BPM = 200
BEAT = 60 / BPM     # 1 = 8분음표
MELODY = [
    ('E5',0.5),('E5',0.5),('E5',1),
    ('C5',0.5),('E5',1),('G5',2),
    ('G4',2),('REST',1),

    ('C5',1.5),('G4',1.5),('E4',1.5),('REST',0.5),
    ('A4',1),('B4',1),('As4',1),('A4',1),
    ('G4',0.75),('E5',0.75),('G5',1),('A5',2),
    ('F5',1),('G5',1),('REST',1),

    ('E5',1),('C5',0.5),('D5',0.5),('B4',1),('REST',1)
]

def led_all_off():
    GPIO.output(COLORS, GPIO.HIGH)

def play_note(note):
    freq = FREQ[note]
    if freq == 0:          # REST
        pwm.ChangeDutyCycle(0)
    else:
        pwm.ChangeFrequency(freq)
        pwm.ChangeDutyCycle(50)   # 50 % 사각파

try:
    playing = False
    idx = 0
    next_time = 0
    prev_btn = GPIO.input(BUTTON)

    while True:
        now = time.monotonic()
        cur_btn = GPIO.input(BUTTON)

        # ─ 버튼 토글 ─
        if prev_btn and not cur_btn:          # 하강-에지
            if not playing:                   # 재생 시작
                print("▶ Start")
                pwm.start(50)
                playing, idx, next_time = True, 0, now
            else:                             # 정지
                print("■ Stop")
                playing = False
                pwm.stop(); led_all_off()
        prev_btn = cur_btn

        # ─ 멜로디 진행 ─
        if playing and now >= next_time:
            note, length = MELODY[idx]
            play_note(note)

            led_all_off()
            GPIO.output(COLORS[idx % 3], GPIO.LOW)   # 순환 LED

            next_time = now + length * BEAT
            idx = (idx + 1) % len(MELODY)

        time.sleep(0.002)

except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    led_all_off()
    GPIO.cleanup()
    print("종료")
