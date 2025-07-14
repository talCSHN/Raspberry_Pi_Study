import RPi.GPIO as GPIO, time

# ── 핀 매핑 ────────────────────────────
RED, GREEN, BLUE = 14, 15, 18
BUTTON, PIEZO    = 17, 25

GPIO.setmode(GPIO.BCM)
GPIO.setup([RED, GREEN, BLUE], GPIO.OUT, initial=GPIO.HIGH)   # HIGH = LED OFF
GPIO.setup(PIEZO, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pwm = GPIO.PWM(PIEZO, 440)

# ── 주파수 테이블 (필요 음만) ────────────
F = {
    'C4':262,'Cs4':277,'D4':294,'Ds4':311,'E4':330,'F4':349,'Fs4':370,
    'G4':392,'Gs4':415,'A4':440,'As4':466,'B4':494,
    'C5':523,'Cs5':554,'D5':587,'Ds5':622,'E5':659,'F5':698,'Fs5':740,
    'G5':784,'Gs5':831,'A5':880,'As5':932,'B5':988
}

# ── 마리오 오버월드 1절 (간략화) ─────────
BPM  = 200
BEAT = 60 / BPM

'''
MELODY = [
    ('E5',0.125),('E5',0.125),('E5',0.25),('C5',0.125),('E5',0.25),('G5',0.25),('G4',0.25),
    (None,0.125),
    ('C5',0.25),('G4',0.25),('E4',0.25),
    (None,0.125),
    ('A4',0.125),('B4',0.125),('As4',0.125),('A4',0.125),
    ('G4',0.125),('E5',0.125),('G5',0.125),('A5',0.25),
    ('F5',0.125),('G5',0.125),
    (None,0.125),
    ('E5',0.25),('C5',0.125),('D5',0.125),('B4',0.25),
    (None,0.25),
    ('C5',0.25),('G4',0.25),('E4',0.25),
    (None,0.125),
    ('A4',0.125),('B4',0.125),('As4',0.125),('A4',0.125),
    ('G4',0.125),('E5',0.125),('G5',0.125),('A5',0.25),
    ('F5',0.125),('G5',0.125),
    (None,0.125),
    ('E5',0.25),('C5',0.125),('D5',0.125),('B4',0.25),
    (None,0.25)
]
'''
MELODY = [
    # ⬇︎ “뚜↗️뚜↘︎뚜↗️   뚜↗️뚜↘︎뚜↗️ … ” (1–2마디)
    ('E5',0.125),('E5',0.125),('E5',0.25),
    ('C5',0.125),('E5',0.25),('G5',0.5),
    ('G4',0.5),(None,0.25),

    # (3–4마디)
    ('C5',0.375),('G4',0.375),('E4',0.375),
    (None,0.125),
    ('A4',0.25),('B4',0.25),('As4',0.25),('A4',0.25),
    ('G4',0.1875),('E5',0.1875),('G5',0.25),('A5',0.5),
    ('F5',0.25),('G5',0.25),(None,0.25),

    # (5–6마디)
    ('E5',0.25),('C5',0.125),('D5',0.125),('B4',0.25),
    (None,0.25),
    ('C5',0.375),('G4',0.375),('E4',0.375),
    (None,0.125),
    ('A4',0.25),('B4',0.25),('As4',0.25),('A4',0.25),
    ('G4',0.1875),('E5',0.1875),('G5',0.25),('A5',0.5),
    ('F5',0.25),('G5',0.25),(None,0.25),

    # (7–8마디, 끝 맺음)
    ('E5',0.25),('C5',0.125),('D5',0.125),('B4',0.25),
    (None,0.25)
]
COLORS = [RED, GREEN, BLUE]  # LED 순환용

# ── 헬퍼 ───────────────────────────────
def led_off(): GPIO.output([RED,GREEN,BLUE], GPIO.HIGH)

# ── 상태 변수 ──────────────────────────
playing, idx, note_end = False, 0, 0
prev_btn = GPIO.input(BUTTON)

try:
    while True:
        now = time.monotonic()

        # 버튼 토글
        curr_btn = GPIO.input(BUTTON)
        if prev_btn == GPIO.HIGH and curr_btn == GPIO.LOW:
            if not playing:              # ▶ 재생
                playing, idx = True, 0
                note_end = now
                pwm.start(50)
                print("PLAY")
            else:                        # ■ 정지
                playing = False
                pwm.stop(); led_off()
                print("STOP")
        prev_btn = curr_btn

        # 재생 루프(무한 반복)
        if playing and now >= note_end:
            note, ln = MELODY[idx]
            if note:  pwm.ChangeFrequency(F[note])
            led_off(); GPIO.output(COLORS[idx % 3], GPIO.LOW)
            note_end = now + ln * BEAT
            idx = (idx + 1) % len(MELODY)   # 끝나면 처음으로

        time.sleep(0.005)  # 5 ms 루프

except KeyboardInterrupt:
    pwm.stop(); led_off(); GPIO.cleanup()
