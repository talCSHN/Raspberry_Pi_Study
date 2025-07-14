import RPi.GPIO as GPIO
import time

# ── 핀 정의 ───────────────────────
RED, GREEN, BLUE = 14, 15, 18
BUTTON = 17
PIEZO = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup([RED, GREEN, BLUE], GPIO.OUT, initial=GPIO.HIGH)  # HIGH = 꺼짐
GPIO.setup(PIEZO, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pwm = GPIO.PWM(PIEZO, 440)  # 초기 주파수
COLORS = [RED, GREEN, BLUE]

# ── 주파수 테이블 ─────────────────
FREQS = {
    'C4':262,'Cs4':277,'D4':294,'Ds4':311,'E4':330,'F4':349,'Fs4':370,
    'G4':392,'Gs4':415,'A4':440,'As4':466,'B4':494,
    'C5':523,'Cs5':554,'D5':587,'Ds5':622,'E5':659,'F5':698,'Fs5':740,
    'G5':784,'Gs5':831,'A5':880,'As5':932,'B5':988
}

# ── Super Mario Overworld Theme (1-A 루프) ──
BPM = 200
BEAT = 60 / BPM

MELODY = [
    ('E5',0.125),('E5',0.125),('E5',0.25),
    ('C5',0.125),('E5',0.25),('G5',0.5),
    ('G4',0.5),(None,0.25),

    ('C5',0.375),('G4',0.375),('E4',0.375),(None,0.125),
    ('A4',0.25),('B4',0.25),('As4',0.25),('A4',0.25),
    ('G4',0.1875),('E5',0.1875),('G5',0.25),('A5',0.5),
    ('F5',0.25),('G5',0.25),(None,0.25),

    ('E5',0.25),('C5',0.125),('D5',0.125),('B4',0.25),(None,0.25),
    ('C5',0.375),('G4',0.375),('E4',0.375),(None,0.125),
    ('A4',0.25),('B4',0.25),('As4',0.25),('A4',0.25),
    ('G4',0.1875),('E5',0.1875),('G5',0.25),('A5',0.5),
    ('F5',0.25),('G5',0.25),(None,0.25),

    ('E5',0.25),('C5',0.125),('D5',0.125),('B4',0.25),(None,0.25)
]

# ── LED 제어 함수 ──────────────────
def led_off():
    GPIO.output([RED, GREEN, BLUE], GPIO.HIGH)

# ── 상태 변수 ──────────────────────
playing = False
note_idx = 0
note_end = 0
prev_btn = GPIO.input(BUTTON)

try:
    while True:
        now = time.monotonic()
        curr_btn = GPIO.input(BUTTON)

        # ─ 버튼 눌림 처리 (토글)
        if prev_btn == GPIO.HIGH and curr_btn == GPIO.LOW:
            if not playing:
                print("▶ 재생 시작")
                pwm.start(50)
                playing = True
                note_idx = 0
                note_end = now
            else:
                print("■ 정지")
                playing = False
                pwm.stop()
                led_off()
        prev_btn = curr_btn

        # ─ 멜로디 재생
        if playing and now >= note_end:
            note, length = MELODY[note_idx]
            if note is not None:
                pwm.ChangeFrequency(FREQS[note])
            else:
                pwm.ChangeFrequency(1)  # 무음 처리
            # LED 효과: 빨–초–파 순환
            led_off()
            GPIO.output(COLORS[note_idx % 3], GPIO.LOW)
            note_end = now + length * BEAT
            note_idx = (note_idx + 1) % len(MELODY)

        time.sleep(0.005)

except KeyboardInterrupt:
    print("\n종료합니다.")
    pwm.stop()
    led_off()
    GPIO.cleanup()
